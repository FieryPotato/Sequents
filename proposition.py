"""
Module containing proposition classes. 

Propositions are immutable hashable objects with the following 
properties:

- 'arity': a measure of how many subpropositions the proposition 
contains.  Atoms and negations are unary (arity=1), while conjunctions, 
disjunctions, and conditionals are binary (arity=2).
- 'symb': the string symbolizing the logical content of the proposition.
The following correspond to propositions in the expected way: &, v, ~, 
->. (Atoms have no logical content and are therefore associated with the 
empty string ('').)
- 'complexity': a measure of how deeply nested the most-nested 
subproposition is. This is measured recursively for each proposition and
subproposition, with Atoms having complexity 0.
- Binary propositions have a 'left' and 'right' property, corresponding 
to the subproposition on that side of their main connective. Negations
meanwhile have the 'negatum' property and Atoms, 'prop'. These can be 
accessed class-agnostically by accessing the object's .content property.

Notably, Atoms have strings as their propositional content, while all
other propositions have Propositions (atoms or otherwise) as their 
content.

Note that for most uses, you should prefer creating the classes in this 
module by using the functions in the convert module (e.g., 
string_to_proposition) over creating these classes directly.
"""

__all__ = ['Atom', 'Negation', 'Conjunction', 'Conditional', 'Disjunction']

import regex

from abc import ABC, abstractmethod
from dataclasses import dataclass

SIDES: set[str] = {'ant', 'con'}
names_re = regex.compile(r'\<(.*)\>')

@dataclass(frozen=True, slots=True)
class Proposition(ABC):
    """
    Base class from which propositions should inherit.
    """
    arity = None  # How many propositions this object contains.
    symb = None  # The logical symbol this object assumes.

    def __post_init__(self) -> None:
        self.validate_content()

    def __getitem__(self, index) -> 'Proposition':
        """
        Allows slicing into self, e.g.:
        >>> p, q = Atom('proposition'), Atom('another_prop')
        >>> cj = Conjunction(p, q)
        >>> cj[0] == p == cj.left
        True
        >>> cj[1] == q == cj.right
        True
        """
        return self.content[index]

    @abstractmethod
    def content(self) -> tuple:
        """Return this object's propositional content."""

    @property
    def complexity(self) -> int:
        """Return this object's logical complexity."""
        return 1 + max(p.complexity for p in self.content)

    @abstractmethod
    def validate_content(self) -> None:
        """Raise ValueError if content has incorrect type."""


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
        return f'({str(self[0])} {self.symb} {str(self[1])})'

    @property
    def content(self) -> tuple[Proposition, Proposition]:
        return self.left, self.right

    def validate_content(self) -> None:
        for prop in self.content:
            if not isinstance(prop, Proposition):
                raise TypeError(
                    f'{self.__class__} content requires propositions, not {type(prop)}.'
                )


@dataclass(slots=True, frozen=True)
class Atom(Proposition):
    """
    Proposition class with no logical content.
    """
    prop: str
    symb = ''
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
            
    def names(self) -> tuple[str]:
        names = regex.search(names_re, self.content[0]).group(1)
        return tuple(n for n in names.split(', ') if len(n) > 1)

    def unbound_variables(self) -> tuple[str]:
        pass


@dataclass(slots=True, frozen=True)
class Negation(Proposition):
    """
    Unary proposition signifying logical 'not ...'.
    """
    negatum: Proposition
    symb = '~'
    arity = 1

    def __str__(self) -> str:
        return f'~ {str(self[0])}'

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

