from abc import ABC, abstractmethod

from proposition import Proposition, Atom,  Conjunction, Conditional,\
        Disjunction, Negation
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
    # While string is bookended by parentheses.
    if not string:
        return ''
    while string[0] == '(' and string[-1] == ')':
        nestedness = 0
        for i, char in enumerate(string):

            # nestedness += 1 for each '('
            # nestedness -= 1 for each ')'
            # no change for any other character
            nestedness += NEST_MAP[char] if char in NEST_MAP else 0

            # If the first and last parentheses are not connected
            # eg. (A v B) -> (C & D)
            if nestedness <= 0 and ((i + 1) < len(string)):
                return string
        else:
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
            fac = ConjunctionFactory()
        case [left, '->' | 'implies', right]:
            fac = ConditionalFactory()
        case [left, 'v' | 'or', right]:
            fac = DisjunctionFactory()
        case ['~' | 'not', negatum]:
            fac = NegationFactory()
        case '':
            return None
        case _:
            fac = AtomFactory()
    return fac.get_prop(*split_string)


def find_connective(string: str) -> list[str]:
    """
    Return a list of strings separating the connective from 
    surrounding propositional material. Deparenthesizes sub-
    propositions.

    >>> Proposition.find_connective('A & B')
    ['A', '&', 'B']
    >>> Proposition.find_connective('not C')
    ['not', 'C']
    >>> Proposition.find_connective('anything')
    ['anything']
    """
    if not string: 
        return ''
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
        if word[0] == '(': nestedness += 1
        if word[-1] == ')': nestedness -= 1

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
    if (split_ants := ant_str.split(',')) != '':
        for ant in split_ants:
            prop = string_to_proposition(ant.strip(' '))
            antecedents.append(prop)

    # Convert consequents
    consequents = []
    if (split_cons := con_str.split(',')) != '':
        for con in split_cons:
            prop = string_to_proposition(con.strip(' '))
            consequents.append(prop)

    antecedent, consequent = tuple(antecedents), tuple(consequents)
	
    return Sequent(
        antecedent,
        consequent
    )


class PropositionFactory(ABC):
    """Abstract Class for proposition factories."""

    @abstractmethod
    def get_prop(self, *content) -> Proposition:
        """Return an instance of the correct proposition."""


class AtomFactory(PropositionFactory):
    """Factory for Atoms."""

    def get_prop(self, content) -> Atom:
        """Return an Atom instance."""
        return Atom(content)


class NegationFactory(PropositionFactory):
    """Factory for Negations."""

    def get_prop(self, _, prop) -> Negation:
        """Return a Negation instance."""
        return Negation(string_to_proposition(prop))


class ConjunctionFactory(PropositionFactory):
    """Factory for Conjunctions."""

    def get_prop(self, left, _, right) -> Conjunction:
        """Return a Conjunction instance."""
        return Conjunction(
            string_to_proposition(left),
            string_to_proposition(right)
        )


class DisjunctionFactory(PropositionFactory):
    """Factory for Disjunctions."""

    def get_prop(self, left, _, right) -> Disjunction:
        """Return a Disjunction instance."""
        return Disjunction(
            string_to_proposition(left),
            string_to_proposition(right)
        )


class ConditionalFactory(PropositionFactory):
    """Factory for Conditionals."""

    def get_prop(self, ant, _, con) -> Conditional:
        """Return a Conditional instance."""
        return Conditional(
            string_to_proposition(ant),
            string_to_proposition(con)
        )

