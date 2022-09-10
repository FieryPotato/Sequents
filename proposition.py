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

import re

from abc import ABC, abstractmethod
from dataclasses import dataclass

SIDES: set[str] = {'ant', 'con'}

# Match anything between angle brackets ('<' and '>')
objects_re = re.compile(r'\<(.*)\>')

# Match anything before an opening angle bracket ('<')
predicate_re = re.compile(r'(.+)\<')

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

    @property
    def names(self) -> tuple[str]:
        """Return a tuple of names in self.content."""
        names = []
        for prop in self.content:
            names.extend([n for n in prop.names])
        return tuple(names)

    @property
    def unbound_variables(self) -> tuple[str]:
        """Return a tuple of unbound variables in self.content."""
        variables = []
        for prop in self.content:
            variables.extend([v for v in prop.unbound_variables])
        return tuple(variables)

    def instantiate(self, variable, name) -> 'cls':
        """
        Return an instance of this class whose instances of variable
        are replaced with name.
        """
        props = [prop.instantiate(variable, name) for prop in self.content]
        return self.__class__(*props)


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
    
    @property
    def objects(self) -> list[str]:
        """
        Return the objects (i.e. names and variables) in self.content.
        """
        result = re.search(objects_re, self.content[0])
        string = result.group(1)
        return string.split(', ')

    @property
    def predicates(self) -> list[str]:
        """Return self.content's predicate."""
        result = re.search(predicate_re, self.content[0])
        string = result.group(1)
        return [string]
            
    @property
    def names(self) -> tuple[str]:
        """Return a tuple of names in self.content."""
        objects: list[str] = self.objects
        return tuple(o for o in objects if len(o) > 1)

    @property
    def unbound_variables(self) -> tuple[str]:
        """Return a tuple of unbound variables in self.content."""
        objects: list[str] = self.objects
        return tuple(o for o in objects if len(o) == 1)

    def instantiate(self, variable: str, name: str) -> 'Atom':
        """
        Return an atom whose instances of variable are replaced with
        name.
        """
        objects: list[str] = self.objects

        # Replace variable instances with name
        new_objects = []
        for o in objects:
            if o == variable:
                o = name
            new_objects.append(o)

        # Put new objects into a new string for Atom creation
        new_content = f"{self.predicates[0]}<{', '.join(new_objects)}>"

        return Atom(new_content)
        



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

