from typing import Protocol

from proposition import Proposition, Atom, Negation, Conjunction,\
    Disjunction, Conditional
from sequent import Sequent

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
    # Return early if there is not string.
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


def string_to_proposition(string) -> Proposition: 
    """
    Convert input string into proposition of the appropriate type.
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
        case '':
            raise ValueError('Cannot convert empty string to proposition.')
        case _:
            fac = AtomFactory
    return fac().get_prop(*split_string)


def find_connective(string: str) -> list[str]:
    """
    Return a list of strings separating the main connective from 
    surrounding propositional material. Deparenthesizes sub-
    propositions.

    >>> find_connective('A & B')
    ['A', '&', 'B']
    >>> find_connective('(A -> B) v (B -> A)')
    ['(A -> B)', 'v', '(B -> A)']
    >>> find_connective('not C')
    ['not', 'C']
    >>> find_connective('anything')
    ['anything']
    """
    # Return early if the string is empty.
    if not string: 
        return ''

    # connective keywords
    negations = {'~', 'not'}
    binaries = {'&', 'v', 'and', 'or', '->', 'implies'}

    word_list = string.split(' ')

    # Check for negation as main connective.
    if word_list[0] in negations:
        sub_prop = ' '.join(word_list[1:])
        return [word_list[0], deparenthesize(sub_prop)]

    # Check for binary connectives as main connective.
    nestedness = 0
    for i, word in enumerate(word_list):

        # Increase nestedness with each '('
        # Decrease nestedness with each ')'
        # No change for other characters.
        nestedness += 1 if word.startswith('(') else 0
        nestedness -= 1 if word.endswith(')') else 0

        if (connective := word) in binaries and nestedness == 0:
            l = deparenthesize(' '.join(word_list[:i]))
            r = deparenthesize(' '.join(word_list[i+1:]))
            return [l, connective, r]

    return [string]


def string_to_sequent(string: str) -> Sequent:
    """
    Return a sequent from input string.
    """
    ant_str, con_str = string.split(';')

    # Convert antecedents
    antecedents = []
    split_ants: list[str] = ant_str.split(',')
    for ant in split_ants:
        # Ignore empty strings.
        if not (ant := ant.strip(' ')):
            break
        antecedents.append(string_to_proposition(ant))

    # Convert consequents
    consequents = []
    split_cons: list[str] = con_str.split(',')
    for con in split_cons:

        # Ignore empty strings.
        if not (con := con.strip(' ')):
            break
        consequents.append(string_to_proposition(con))

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

