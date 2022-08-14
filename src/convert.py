from src.proposition import Proposition, Atom,  Conjunction, Conditional,\
        Disjunction, Negation
from src.sequent import Sequent

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
    broken_string: list[str] = find_connective(string)
    match broken_string:
        case [left, '&' | 'and', right]:
            return Conjunction(
                string_to_proposition(left),
                string_to_proposition(right)
            )
        case [left, '->' | 'implies', right]:
            return Conditional(
                string_to_proposition(left),
                string_to_proposition(right)
            )
        case [left, 'v' | 'or', right]:
            return Disjunction(
                string_to_proposition(left),
                string_to_proposition(right)
            )
        case ['~' | 'not', negatum]:
            return Negation(string_to_proposition(negatum))
        case [proposition]:
            return Atom(proposition)
        case _:
            return


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
    antecedent = [string_to_proposition(s.strip(' ')) for s in ant_str.split(',')]
    consequent = [string_to_proposition(s.strip(' ')) for s in con_str.split(',')]
    return Sequent(
        antecedent,
        consequent
    )

