from abc import ABC, abstractmethod
from dataclasses import dataclass

SIDES: set[str] = {'ant', 'con'}


@dataclass(frozen=True, order=True)
class Proposition(ABC):
    """
    Base class for propositions.
    """
    left = None
    right = None
    arity = None
    symb = None

    def __post_init__(self) -> None:
        self.validate_content()

    def __getitem__(self, index) -> 'Proposition':
        return self.content[index]

    @abstractmethod
    def content(self) -> tuple:
        """Return this object's propositional content."""

    @property
    def complexity(self) -> int:
        return 1 + max(p.complexity for p in self.content)

    @abstractmethod
    def validate_content(self) -> None:
        """Raises error if content has incorrect type."""


@dataclass(slots=True, frozen=True)
class BinaryProposition(Proposition):
    """
    Super class for binary propositions.
    """
    left: Proposition
    right: Proposition
    arity = 2
    symb = None

    def __str__(self):
        return f'({self[0]} {self.symb} {self[1]})'

    def validate_content(self) -> None:
        for prop in self.content:
            if not isinstance(prop, Proposition):
                raise TypeError(
                    f'{self.__class__} content requires propositions, not {type(prop)}.'
                )

    @property
    def content(self) -> tuple[Proposition, Proposition]:
        return self.left, self.right


@dataclass(slots=True, frozen=True)
class Atom(Proposition):
    """
    Proposition class with no logical content.
    """
    symb = ''
    prop: str
    arity = 1

    def __str__(self) -> str:
        return f'{self[0]}'

    @property
    def complexity(self) -> int:
        return 0

    @property
    def content(self) -> tuple[str]:
        return self.prop,

    def validate_content(self) -> None:
        if not isinstance(self.prop, str):
            raise TypeError(
                f'{self.__class__} content requires string, not {type(self.prop)}.'
            )


@dataclass(slots=True, frozen=True)
class Negation(Proposition):
    """
    Unary proposition signifying logical 'not ...'.
    """
    negatum: Proposition
    symb = '~'
    arity = 1

    def __str__(self) -> str:
        return f'~ ({self[0]})'

    @property
    def content(self) -> tuple[Proposition]:
        return self.negatum,

    def validate_content(self) -> None:
        if not isinstance(self.negatum, Proposition):
            raise TypeError(
                f'{self.__class__} content requires Proposition, not {type(self.negatum)}.'
            )


@dataclass(slots=True, frozen=True)
class Conjunction(BinaryProposition):
    """
    Binary proposition signifying logical '... and ...'.
    """
    symb = '&'


@dataclass(slots=True, frozen=True)
class Conditional(BinaryProposition):
    """
    Binary proposition signifying logical 'if ... then ...'
    """
    symb = '->'


@dataclass(slots=True, frozen=True)
class Disjunction(BinaryProposition):
    """
    Binary proposition signifying logical '... or ...'
    """
    symb = 'v'
