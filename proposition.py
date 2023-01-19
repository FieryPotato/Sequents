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

- 'word': the string which corresponds to self.symb in natural language.

- 'complexity': a measure of how deeply nested the most-nested
subproposition is. This is measured recursively for each proposition and
subproposition, with Atoms having complexity 0.

- Binary propositions have a 'left' and 'right' property, corresponding
to the subproposition on that side of their main connective. Negations
meanwhile have the 'negatum' property and Atoms, 'prop'. These can be
accessed class-agnostically by accessing the object's .content property.

- names: a tuple of strings containing each name in the proposition and
subpropositions. Names are always two or more lowercase letters.

- unbound_variables: a tuple of strings containing each unbound variable
in the proposition. Unbound variables are single lowercase letters not
bound by a quantifier.

- instantiate: return this proposition with all instances of a variable
replaced with a name. If the proposition is a quantifier and the
variable, is the variable it binds, instead return the subproposition
(i.e. remove the quantifier).

Notably, Atoms have strings as their propositional content, while all
other propositions have Propositions (atoms or otherwise) as their
content.

Note that for most uses, you should prefer creating the classes in this
module by using the functions in the convert module (e.g.,
string_to_proposition) over creating these classes directly.
"""

__all__ = ['Atom', 'Negation', 'Conjunction', 'Conditional', 'Disjunction',
           'Proposition', 'Universal', 'Existential']

import re

from abc import ABC, abstractmethod
from dataclasses import dataclass
# from typing import Self
from typing import TypeVar

SIDES: set[str] = {'ant', 'con'}

# Match anything between angle brackets ('<' and '>')
objects_re = re.compile(r'<(.*)>')

# Match anything before an opening angle bracket ('<')
predicate_re = re.compile(r'(.+)<')

Self = TypeVar('Self')


@dataclass(frozen=True, slots=True, order=True)
class Proposition(ABC):
    """
    Base class from which propositions should inherit.
    """
    arity = None  # How many propositions this object contains.
    symb = None  # The logical symbol this object assumes.
    word = None  # The english language word representing self.symb.

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

    @property
    @abstractmethod
    def long_string(self) -> str:
        """
        Return this proposition's string with connective symbols
        expanded to their whole words.
        """

    @property
    @abstractmethod
    def content(self) -> tuple:
        """Return this object's propositional content."""

    @property
    def complexity(self) -> int:
        """Return this object's logical complexity."""
        return 1 + max(p.complexity for p in self.content)

    def validate_content(self) -> None:
        """Raise ValueError if content has incorrect type."""
        for prop in self.content:
            if not isinstance(prop, Proposition):
                raise TypeError(
                    f'{self.__class__} content requires propositions, not {type(prop)}.'
                )

    @property
    def names(self) -> set[str]:
        """Return a tuple of names in self.content."""
        return {name for prop in self.content for name in prop.names}

    @property
    def unbound_variables(self) -> tuple[str]:
        """Return a tuple of unbound variables in self.content."""
        variables = set()
        for prop in self.content:
            variables.update(set(prop.unbound_variables))

        return tuple(sorted(variables))

    def instantiate(self, variable, name) -> Self:
        """
        Return an instance of this class whose instances of variable
        are replaced with name.
        """
        props = [prop.instantiate(variable, name) for prop in self.content]
        return self.__class__(*props)


@dataclass(slots=True, frozen=True, order=True)
class UnaryProposition(Proposition):
    """
    Super class for unary propositions.
    """
    prop: Proposition
    arity = 1
    symb = None
    word = None
    variable = ''

    def __str__(self) -> str:
        return f'{self.symb} {self.prop}'

    @property
    def long_string(self) -> str:
        return f'{self.word} {self.prop.long_string}'

    @property
    def content(self) -> tuple[Proposition | str]:
        return self.prop,


@dataclass(slots=True, frozen=True, order=True)
class Quantifier(Proposition):
    """
    Super class for quantifiers.
    """
    variable: str
    prop: Proposition
    arity = 1
    symb = None
    word = None

    def __str__(self) -> str:
        return f'{self.symb}{self.variable} {self.prop}'

    @property
    def long_string(self) -> str:
        return f'{self.word}{self.variable} {self.prop.long_string}'

    @property
    def content(self) -> tuple[Proposition]:
        return self.prop,

    @property
    def unbound_variables(self) -> tuple[str]:
        variables = set()
        for prop in self.content:
            variables.update(set(prop.unbound_variables))
        unbound = [v for v in variables if v != self.variable]
        return tuple(sorted(unbound))

    def instantiate(self, variable, name) -> Proposition:
        """
        Return self with instances of variable replaced with name.
        If variable is self.variable, instead return instantiated 
        subproposition.
        """
        if variable == self.variable:
            return self.instantiate_with(name)
        sub_prop = self.prop.instantiate(variable, name)
        return self.__class__(self.variable, sub_prop)

    def instantiate_with(self, name) -> Self:
        """Return self.prop instantiated with self.variable."""
        return self.prop.instantiate(self.variable, name)


@dataclass(slots=True, frozen=True, order=True)
class BinaryProposition(Proposition):
    """
    Super class for binary propositions.
    """
    left: Proposition
    right: Proposition
    arity = 2
    symb = None
    word = None

    def __str__(self):
        return f'({str(self[0])} {self.symb} {str(self[1])})'

    @property
    def long_string(self) -> str:
        return f'({self[0].long_string} {self.word} {self[1].long_string})'

    @property
    def content(self) -> tuple[Proposition, Proposition]:
        return self.left, self.right


@dataclass(slots=True, frozen=True, order=True)
class Atom(UnaryProposition):
    """
    Proposition class with no logical content.
    """
    prop: str
    arity = 1
    symb = ''
    word = ''

    def __str__(self) -> str:
        return f'{self[0]}'

    @property
    def long_string(self) -> str:
        return str(self)

    @property
    def complexity(self) -> int:
        return 0

    def validate_content(self) -> None:
        if not isinstance(self.prop, str):
            raise TypeError(
                f'{self.__class__} content requires string, not {type(self.prop)}.'
            )

    @property
    def objects(self) -> list[str]:
        """
        Return the objects (i.e. names and variables) in self.content.
        """
        result = re.search(objects_re, self.content[0])
        if result:
            string = result.group(1)
            return string.split(', ')
        return []

    @property
    def predicates(self) -> list[str]:
        """Return self.content's predicate."""
        result = re.search(predicate_re, self.content[0])
        string = result.group(1)
        return [string]

    @property
    def names(self) -> set[str]:
        """Return a tuple of names in self.content."""
        return {o for o in self.objects if len(o) > 1}

    @property
    def unbound_variables(self) -> tuple[str]:
        """Return a tuple of unbound variables in self.content."""
        variables = [o for o in set(self.objects) if len(o) == 1]
        return tuple(sorted(variables))

    def instantiate(self, variable: str, name: str) -> Self:
        """
        Return an atom whose instances of variable are replaced with
        name.
        """
        # Replace variable instances with name
        new_objects = [
            name if o == variable else o for o in self.objects
        ]

        # Put new objects into a new string for Atom creation
        new_content = f"{self.predicates[0]}<{', '.join(new_objects)}>"

        return Atom(new_content)


@dataclass(slots=True, frozen=True, order=True)
class Universal(Quantifier):
    """
    Unary proposition signifying logical 'for all ...'.
    """
    variable: str
    prop: Proposition
    arity = 1
    symb = '∀'
    word = 'forall'


@dataclass(slots=True, frozen=True, order=True)
class Existential(Quantifier):
    """
    Unary proposition signifying logical 'there is at least one ...'.
    """
    variable: str
    prop: Proposition
    arity = 1
    symb = '∃'
    word = 'exists'


@dataclass(slots=True, frozen=True, order=True)
class Negation(UnaryProposition):
    """
    Unary proposition signifying logical 'not ...'.
    """
    prop: Proposition
    symb = '~'
    word = 'not'
    arity = 1


@dataclass(slots=True, frozen=True, order=True)
class Conjunction(BinaryProposition):
    """
    Binary proposition signifying logical '... and ...'.
    """
    symb = '&'
    word = 'and'


@dataclass(slots=True, frozen=True, order=True)
class Conditional(BinaryProposition):
    """
    Binary proposition signifying logical 'if ... then ...'
    """
    symb = '->'
    word = 'implies'


@dataclass(slots=True, frozen=True, order=True)
class Disjunction(BinaryProposition):
    """
    Binary proposition signifying logical '... or ...'
    """
    symb = 'v'
    word = 'or'
