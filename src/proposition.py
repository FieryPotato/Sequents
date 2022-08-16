from abc import ABC, abstractmethod
from collections import namedtuple
from dataclasses import dataclass

SIDES: set[str] = {'ant', 'con'}

tupseq = namedtuple('tupseq', ['ant', 'con'])

@dataclass(frozen=True, order=True)
class Proposition(ABC): 
    """
    Base class for propositions.
    """

    def __post_init__(self) -> None:
        self.validate_content()

    @abstractmethod
    def content(self) -> list:
        """Return this object's propositional content."""
    
    @property
    def complexity(self) -> int:
        return 1 + max(p.complexity for p in self.content) 

    @abstractmethod
    def decomposed(self, side) -> tuple[tupseq]:
        """
        Return results of decomposing an instance of the current
        proposition on input side.
        """

    @abstractmethod
    def validate_content(self) -> None:
        """Raises error if content has incorrect type."""

    class AtomicDecompositionError(Exception):
        def __init__(self, proposition):
            msg = f'{proposition} is an atom and cannot be decomposed.'
            super().__init__(msg)

@dataclass(slots=True, frozen=True)
class BinaryProposition(Proposition):
    """
    Super class for binary propositions.
    """
    left: Proposition
    right: Proposition
    arity = 2

    def __str__(self):
        return f'({self.content[0]} {self.symb} {self.content[1]})'

    def validate_content(self) -> None:
        for prop in self.content:
            if not isinstance(prop, Proposition):
                raise TypeError(
                    f'{self.__class__} content requires propositions, not {type(prop)}.'
                )

    @property
    def content(self) -> list[Proposition, Proposition]:
        return [self.left, self.right]


@dataclass(slots=True, frozen=True)
class Atom(Proposition):
    """
    Proposition class with no logical content.
    """
    prop: str
    arity = 1
    
    def __str__(self) -> str:
        return f'{self.content[0]}'

    @property
    def complexity(self) -> int:
        return 0

    @property
    def content(self) -> list[str]:
        return [self.prop]

    def validate_content(self) -> None:
        if not isinstance(self.prop, str):
            raise TypeError(
                f'{self.__class__} content requires string, not {type(self.prop)}.'
            )

    def decomposed(self, side) -> None:
        raise self.AtomicDecompositionError()


@dataclass(slots=True, frozen=True)
class Negation(Proposition):
    """
    Unary proposition signifying logical 'not ...'.
    """
    negatum: Proposition
    arity = 1

    def __str__(self) -> str:
        return f'(~{self.content[0]})'

    @property
    def content(self) -> list[Proposition]:
        return [self.negatum]

    def validate_content(self) -> None:
        if not isinstance(self.negatum, Proposition):
            raise TypeError(
                f'{self.__class__} content requires Proposition, not {type(self.negatum)}.'
            )

    def decomposed(self, side) -> tuple[tupseq]:
        assert side in SIDES
        if side == 'ant':
            return tupseq([], [self.content[0]]),
        return tupseq([self.content[0]], []),


@dataclass(slots=True, frozen=True)
class Conjunction(BinaryProposition):
    """
    Binary proposition signifying logical '... and ...'.
    """
    symb = '&'

    def decomposed(self, side) -> tuple[tupseq]:
        assert side in SIDES
        if side == 'ant':
            return tupseq(self.content, []),
        return tupseq([], [self.content[0]]), tupseq([], [self.content[1]])


@dataclass(slots=True, frozen=True)
class Conditional(BinaryProposition):
    """
    Binary proposition signifying logical 'if ... then ...'
    """
    symb = '->'
    
    def decomposed(self, side) -> tuple[tupseq]:
        assert side in SIDES
        if side == 'ant':
            return tupseq([], [self.content[0]]), tupseq([self.content[1]], [])
        return tupseq([self.content[0]], [self.content[1]]),


@dataclass(slots=True, frozen=True)
class Disjunction(BinaryProposition):
    """
    Binary proposition signifying logical '... or ...'
    """
    symb = 'v'

    def decomposed(self, side) -> tuple[tupseq]:
        assert side in SIDES
        if side == 'ant':
            return tupseq([self.content[0]], []), tupseq([self.content[1]], [])
        return tupseq([], self.content),

