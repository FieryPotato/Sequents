import re

from src.proposition import Atom, Conditional, Conjunction,\
        Disjunction, Negation, Proposition
from src.sequent import Sequent


re_binary = re.compile(r'(.+)( and | \& | -\> | or | v )(.+)')
re_if = re.compile(r'(if )(.+)( then )(.+)')

CONJUNCTIONS = {' and ', ' & '}
CONDITIONALS = {' -> '}  # 'if ... then ...' omitted for formatting reasons
DISJUNCTIONS = {' or ', ' v '}

class Convert:

    def __init__(self, target) -> None:
        self.target = target

    def to_proposition(self) -> Proposition:
        if result := re.match(re_binary, self.target):
            a, connective, b = result.groups()
            if connective in CONJUNCTIONS:
                return Conjunction(Atom(a), Atom(b))
            elif connective in CONDITIONALS:
                return Conditional(Atom(a), Atom(b))
            elif connective in DISJUNCTIONS:
                return Disjunction(Atom(a), Atom(b))
        elif result := re.match(re_if, self.target):
            _, a, _, b = result.groups()
            return Conditional(Atom(a), Atom(b))
        return Atom(self.target)

