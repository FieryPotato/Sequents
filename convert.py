"""
Package for converting objects of one type to another.
"""

__all__ = [
    'dict_to_tree', 'sequent_to_tree', 'string_to_proposition',
    'string_to_sequent', 'string_to_tree', 'tree_to_dict'
]

from typing import Protocol, Type

import utils

from proposition import Atom, Negation, Universal, Existential, Conjunction, Disjunction, Conditional
from sequent import Sequent
from tree import Tree
from utils import serialize


class Proposition(Protocol):
    ...


def string_to_proposition(string) -> Proposition:
    """
    Convert input string into proposition of the appropriate type.
    Strings are split by their connective i.e.  either the symbol (&, v,
    ->, ~) or the associated word ('and', 'or', 'implies', 'not'). 
    Empty strings raise a value error. If a connective word or symbol
    cannot be matched, an atom with the full string is returned.
    """
    string = utils.deparenthesize(string)
    split_string: list[str] = utils.find_connective(string)

    fac: Type[PropositionFactory]
    match split_string:
        case [left, '&' | 'and', right]:
            fac = ConjunctionFactory
        case [left, '->' | 'implies', right]:
            fac = ConditionalFactory
        case [left, 'v' | 'or', right]:
            fac = DisjunctionFactory
        case ['~' | 'not', negatum]:
            fac = NegationFactory
        case ['∀' | 'forall', var, prop]:
            fac = UniversalFactory
        case ['∃' | 'exists', var, prop]:
            fac = ExistentialFactory
        case '':
            raise ValueError('Cannot convert empty string to proposition.')
        case _:
            fac = AtomFactory
    return fac().get_prop(*split_string)


def sequent_to_tree(sequent: Sequent, names: set = None, grow: bool = True) -> Tree:
    """
    Return a solved tree whose root is the input sequent. 
    """
    if names is None:
        names = set()
    tree = Tree(sequent, names=names)
    if grow:
        tree.grow()
    return tree


def string_to_tree(string: str, names: set = None, grow: bool = True) -> Tree:
    """
    Combines string_to_sequent and string_to_tree as a shortcut for
    calling both functions.
    """
    if names is None: 
        names = set()
    sequent = string_to_sequent(string)
    return sequent_to_tree(sequent, names, grow=grow)


def dict_to_tree(dictionary: dict, is_grown: bool = True) -> Tree:
    """
    Initialize a Tree object from input dictionary. By default, the 
    input dictionary is assumed to contain a fully solved tree, but 
    the is_grown parameter can be set to False to override this 
    behaviour.
    """
    # We know that there is one and only one item in the dict but we
    # do not know its key, so this is the quick way to get it.
    first_key = next(iter(dictionary.keys()))
    tree = Tree(first_key, is_grown=is_grown)
    tree.branches = dictionary
    return tree


def tree_to_dict(tree) -> dict:
    """
    Create a dictionary from a tree.
    """
    return serialize(tree.branches)


def string_to_sequent(string: str) -> Sequent:
    """
    Return a sequent from input string. 

    The string should have its antecedents separated from its 
    consequents by a semicolon, each of its antecedents separated by a
    comma, and likewise for its consequents. Strings without any 
    antecedents can simply start with the semicolon, and sequents 
    without consequents should end with the semicolon with no need for 
    leading or trailing spaces. For example (with linebreaks for clarity):
    >>> string_to_sequent('(A v B), (B -> ~ C); (A & C), B')
    Sequent(
        ant=(
            Disjunction(Atom('A'), Atom('B')), 
            Conditional(Atom('B'), Negation(Atom('C')))
        ),
        con=(
            Conjunction(Atom('A'), Atom('C')), 
            Atom('B')
        )
    )
    """
    # First we split into antecedent and consequent as whole strings
    ant_string, con_string = string.split(';')
    
    # For each side, we split it by comma, and remove whitespace from
    # the extremities. If there's nothing but whitespace, then that 
    # was empty. Otherwise, we turn each string into the proposition
    # it represents

    ant_list: list[str] = [s.strip(' ') for s in ant_string.split(',')]
    if ant_list == ['']:  
        antecedents = []  # Empty list for empty antecedents
    else:
        antecedents = [string_to_proposition(ant) for ant in ant_list]

    con_list: list[str] = [s.strip(' ') for s in con_string.split(',')]
    if con_list == ['']:
        consequents = []  # Empty list for empty consequents
    else:
        consequents = [string_to_proposition(con) for con in con_list]

    return Sequent(
        tuple(antecedents),
        tuple(consequents)
    )


class PropositionFactory(Protocol):
    """Protocol for proposition factories."""

    def get_prop(self, *content) -> Proposition:
        ...


class AtomFactory:
    """Factory for Atoms."""

    def get_prop(self, content) -> Atom:
        """Return an Atom instance."""
        return Atom(content)


class NegationFactory:
    """Factory for Negations."""

    def get_prop(self, _, prop) -> Negation:
        """Return a Negation instance."""
        return Negation(string_to_proposition(prop))


class UniversalFactory:
    """Factory for Universals."""

    def get_prop(self, _, var, prop) -> Universal:
        return Universal(var, string_to_proposition(prop))


class ExistentialFactory:
    """Factory for Existentials."""

    def get_prop(self, _, var, prop) -> Existential:
        return Existential(var, string_to_proposition(prop))


class ConjunctionFactory:
    """Factory for Conjunctions."""

    def get_prop(self, left, _, right) -> Conjunction:
        """Return a Conjunction instance."""
        return Conjunction(
            string_to_proposition(left),
            string_to_proposition(right)
        )


class DisjunctionFactory:
    """Factory for Disjunctions."""

    def get_prop(self, left, _, right) -> Disjunction:
        """Return a Disjunction instance."""
        return Disjunction(
            string_to_proposition(left),
            string_to_proposition(right)
        )


class ConditionalFactory:
    """Factory for Conditionals."""

    def get_prop(self, ant, _, con) -> Conditional:
        """Return a Conditional instance."""
        return Conditional(
            string_to_proposition(ant),
            string_to_proposition(con)
        )