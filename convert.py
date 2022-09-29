"""
Package for converting objects of one type to another.
"""

__all__ = [
    'dict_to_tree', 'sequent_to_tree', 'string_to_proposition', 
    'string_to_sequent', 'string_to_tree'
]

from typing import Protocol

from proposition_factories import PropositionFactory, AtomFactory, NegationFactory, UniversalFactory, \
    ExistentialFactory, ConjunctionFactory, DisjunctionFactory, ConditionalFactory
from sequent import Sequent
from tree import Tree
from utils import deparenthesize, split_branch, find_connective


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
    string = deparenthesize(string)
    split_string: list[str] = find_connective(string)

    fac: PropositionFactory 
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
    first_key = next(iter(dictionary.keys()))
    tree = Tree(first_key, is_grown=is_grown)
    tree.branches = dictionary
    return tree


def tree_to_dict(tree) -> dict:
    """
    Create a dictionary from a tree.
    """
    def serialize(data):
        """Recursively make elements of data json-serializable."""
        result = None
        if isinstance(data, dict):
            result = {str(key): serialize(element) 
                      for key, element in data.items()}
        elif isinstance(data, list):
            result = [serialize(element) for element in data]
        return result
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


def split_tree(tree) -> list[Tree]:
    """
    Return a list of all possible full trees in tree, where a full
    tree consists only of dict[Sequent, dict | None] pairs. All
    non-invertible rules are split into separate trees, which are
    identical until the rule application.
    """
    if (root_parent := tree.branches[tree.root]) is None:
        return [tree]
    result = []
    for sub_tree in split_branch(root_parent):
        new_dict = {tree.root: sub_tree}
        result.append(
            dict_to_tree(new_dict)
        )
    return result
