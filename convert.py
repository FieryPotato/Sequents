"""
Package for converting objects of one type to another.
"""

__all__ = [
    'dict_to_tree', 'sequent_to_tree', 'string_to_proposition',
    'string_to_sequent', 'string_to_tree', 'tree_to_dict'
]

from typing import Protocol, Type


from proposition import Atom, Negation, Universal, Existential, Conjunction, Disjunction, Conditional, Proposition
from sequent import Sequent
from tree import Tree


NEST_MAP = {
    '(': 1,
    ')': -1
}


def string_to_proposition(string) -> Proposition:
    """
    Convert input string into proposition of the appropriate type.
    Strings are split by their connective i.e.  either the symbol (&, v,
    ->, ~) or the associated word ('and', 'or', 'implies', 'not'). 
    Empty strings raise a value error. If a connective word or symbol
    cannot be matched, an atom with the full string is returned.
    """
    string = deparenthesize(string)
    split_string: list[str] = find_connective(string)

    fac: Type[PropositionFactory]
    match split_string:
        case [_, '&' | 'and', _]:
            fac = ConjunctionFactory
        case [_, '->' | 'implies', _]:
            fac = ConditionalFactory
        case [_, 'v' | 'or', _]:
            fac = DisjunctionFactory
        case ['~' | 'not', _]:
            fac = NegationFactory
        case ['∀' | 'forall', _, _]:
            fac = UniversalFactory
        case ['∃' | 'exists', _, _]:
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
    tree = Tree(root=sequent, names=names)
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
    ...


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
        antecedents = ()
    else:
        antecedents = tuple(map(string_to_proposition, ant_list))

    con_list: list[str] = [s.strip(' ') for s in con_string.split(',')]
    if con_list == ['']:
        consequents = ()
    else:
        consequents = tuple(map(string_to_proposition, con_list))

    return Sequent(
        antecedents,
        consequents
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


def find_connective(string: str) -> list[str]:
    """
    Return a list of strings separating the main connective from
    surrounding propositional material. Deparenthesizes sub-
    propositions.

    >>> find_connective('A & B')
    ['A', '&', 'B']
    >>> find_connective('(A -> B) v (B -> A)')
    ['A -> B', 'v', 'B -> A']
    >>> find_connective('not C')
    ['not', 'C']
    >>> find_connective('anything')
    ['anything']
    """
    string = deparenthesize(string)
    # Return early if the string is empty.
    if not string:
        return ['']

    # connective keywords
    negations = {'~', 'not'}
    binaries = {'&', 'v', 'and', 'or', '->', 'implies'}
    quantifiers = {'∃', '∀', 'exists', 'forall'}

    word_list = string.split(' ')

    # Check for negation as main connective.
    if (connective := word_list[0]) in negations:
        negatum = ' '.join(word_list[1:])
        return [connective, deparenthesize(negatum)]

    # Check for quantifiers as main connective.
    # The first slice into word_list finds a word, the second, a letter
    if (connective := word_list[0][:-1]) in quantifiers:
        variable = word_list[0][-1]
        prop = ' '.join(word_list[1:])
        return [connective, variable, deparenthesize(prop)]

    # Check for binary connectives as main connective.
    nestedness = 0
    for i, word in enumerate(word_list):

        for char in word:
            # Increase nestedness with each '('
            # Decrease nestedness with each ')'
            # No change for other characters.
            nestedness += NEST_MAP[char] if char in NEST_MAP else 0

        if (connective := word) in binaries and nestedness == 0:
            left = deparenthesize(' '.join(word_list[:i]))
            right = deparenthesize(' '.join(word_list[i + 1:]))
            return [left, connective, right]

    return [string]


def deparenthesize(string: str) -> str:
    """
    Remove all linked outer parentheses from input string.

    >>> deparenthesize('(one set)')
    'one set'
    >>> deparenthesize('((two sets))')
    'two sets'
    >>> deparenthesize('(nested (sets))')
    'nested (sets)'
    >>> deparenthesize('(unconnected) (sets)')
    '(unconnected) (sets)'
    """
    # Return early if the string is empty.
    if not string:
        return ''

    # While string is bookended by parentheses.
    while string.startswith('(') and string.endswith(')'):

        # Ensure outer parentheses are connected
        nestedness = 0
        for index, char in enumerate(string):

            # Increase nestedness with each '('
            # Decrease nestedness with each ')'
            # No change otherwise.
            nestedness += NEST_MAP[char] if char in NEST_MAP else 0

            # If the first and last parentheses are not connected
            # eg. (A v B) -> (C & D)
            if nestedness <= 0 and ((index + 1) < len(string)):
                return string

        # If they are connected, remove them and check again.
        string = string[1:-1]

    return string


