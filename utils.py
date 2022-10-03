"""
Package containing a bunch of functions that might be useful enough
not to hide away in some other file, and which mainly operate on
builtin data types (dict, str, etc.). Most of these started out as
inner functions that become more complex than just a line or two.
"""
import itertools
from typing import Generator

NEST_MAP = {'(': 1, ')': -1}


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
        for i, char in enumerate(string):

            # Increase nestedness with each '('
            # Decrease nestedness with each ')'
            # No change otherwise.
            nestedness += NEST_MAP[char] if char in NEST_MAP else 0

            # If the first and last parentheses are not connected
            # eg. (A v B) -> (C & D)
            if nestedness <= 0 and ((i + 1) < len(string)):
                return string

        # If they are connected, remove them and check again.
        string = string[1:-1]

    return string


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


def count_dict_branches(d: dict) -> int:
    """
    Return the number of branches in d. Fails for dicts containing
    anything other than dict[dict|None] (i.e. no lists). In the context
    of trees, this counts the trees axioms.
    """
    total = len(parents := d.values())
    for parent in parents:
        if isinstance(parent, dict):
            # We subtract 1 because the number of branches is constant
            # for one-parent connectives, but increases by one for two-
            # parent connectives.
            total += (count_dict_branches(parent) - 1)
    return total


def split_branch(branch: dict | list) -> list[dict]:
    """
    Functions as a switch statement for tree splitting algorithms based
    on whether the input was a dict or list.
    """
    if isinstance(branch, dict):
        return [split_tree_dict(branch)]
    if isinstance(branch, list):
        return split_tree_list(branch)


def split_tree_dict(branch: dict) -> dict:
    """
    Does the work for split_tree if the branch is a dict.
    """
    sub_result = {}
    for sequent, sub_tree in branch.items():
        if (sub_branch := branch[sequent]) is None:
            sub_result[sequent] = None
        else:
            sub_result[sequent] = {sequent: r for r in split_branch(sub_branch)}
    return sub_result


def split_tree_list(branches: list) -> list[dict]:
    """
    Does the work for split_tree if the branch is a list.
    """
    result = []
    for branch in branches:
        result.extend(split_branch(branch))
    return result


def serialize(data: list | dict) -> list | dict:
    """
    Recursively make elements of data json-serializable.
    """
    result = None
    if isinstance(data, dict):
        result = {str(key): serialize(element)
                  for key, element in data.items()}
    elif isinstance(data, list):
        result = [serialize(element) for element in data]
    return result


def binary_combinations(data: tuple) -> Generator[tuple[tuple, tuple], None, None]:
    """
    Yields all possible ways to split input data into two groups.
    """
    # Represent which parent had the proposition by allocating True
    # to one and false to the other (in all combinations).
    combinations = itertools.product([True, False], repeat=len(data))
    for combination in combinations:
        x = [data[i] for i, v in enumerate(combination) if v]
        y = [data[i] for i, v in enumerate(combination) if not v]
        yield tuple(x), tuple(y)
