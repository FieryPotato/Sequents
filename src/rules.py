from abc import ABC, abstractmethod

from src.proposition import Proposition
from src.sequent import Sequent


class Rule(ABC):
    """Abstract class for rules."""

    def __init__(self, sequent: Sequent) -> None:
        self.sequent = sequent

    def apply(self) -> list[Sequent]:
        """Apply this rule to self.sequent."""
        prop, side, index = self.sequent.first_complex_prop
        decomposed: list[Sequent] = self.decompose(prop)

        results = []
        for sequent in decomposed:
            new = self.sequent.remove(side, index)
            results.append(Sequent.mix(new, sequent))

        return results

    @abstractmethod
    def decompose(self, prop: Proposition) -> list[Sequent]:
        """Return sequents resulting from decomposing prop."""

class LNeg(Rule):
    def decompose(self, prop: Proposition) -> list[Sequent]:
        """Apply left negation rule to self.sequent."""
        return [Sequent(tuple(), (prop.content[0],))]

class RNeg(Rule):
    def decompose(self, prop: Proposition) -> list[Sequent]:
        """Apply right negation rule to self.sequent."""
        return [Sequent((prop.content[0],), tuple())]        

class MultLAnd(Rule):
    def decompose(self, prop: Proposition) -> list[Sequent]:
        """Apply multiplicative left conjunction rule to self.sequent."""
        return [Sequent(prop.content, tuple())]

class AddLAnd(Rule):
    def decompose(self, prop: Proposition) -> list[Sequent]:
        """Apply additive left conjunction rule to self.sequent."""
        pass

class MultRAnd(Rule):
    def decompose(self, prop: Proposition) -> list[Sequent]:
        """Apply multiplicative right conjunction rule to self.sequent."""
        pass

class AddRAnd(Rule):
    def decompose(self, prop: Proposition) -> list[Sequent]:
        """Apply additive right conjunction rule to self.sequent."""
        return [
            Sequent(tuple(), (prop.left,)),
            Sequent(tuple(), (prop.right,))
        ]

class MultLOr(Rule):
    def decompose(self, prop: Proposition) -> list[Sequent]:
        """Apply multiplicative left disjunction rule to self.sequent."""
        pass

class AddLOr(Rule):
    def decompose(self, prop: Proposition) -> list[Sequent]:
        """Apply additive left disjunction rule to self.sequent."""
        return [
            Sequent((prop.left,), tuple()),
            Sequent((prop.right,), tuple())
        ]

class MultROr(Rule):
    def decompose(self, prop: Proposition) -> list[Sequent]:
        """Apply multiplicative right disjunction rule to self.sequent."""
        return [Sequent(tuple(), prop.content)]

class AddROr(Rule):
    def decompose(self, prop: Proposition) -> list[Sequent]:
        """Apply additive right disjunction rule to self.sequent."""
        pass

class MultLIf(Rule):
    def decompose(self, prop: Proposition) -> list[Sequent]:
        """Apply multiplicative left conditional rule to self.sequent."""
        pass

class AddLIf(Rule):
    def decompose(self, prop: Proposition) -> list[Sequent]:
        """Apply additive left conditional rule to self.sequent."""
        return [
            Sequent(tuple(), (prop.left,)),
            Sequent((prop.right,), tuple())   
        ] 

class MultRIf(Rule): 
    def decompose(self, prop: Proposition) -> list[Sequent]: 
        """Apply multiplicative right conditional rule to self.sequent.""" 
        return [Sequent((prop.left,), (prop.right,))]

class AddRIf(Rule):
    def decompose(self, prop: Proposition) -> list[Sequent]:
        """Apply additive right conditional rule to self.sequent."""
        pass

# Ketonen rules are used by default.
DEFAULTS = {
    '~': {
        'ant': 'mul',
        'con': 'mul',
    },
    '&': {
        'ant': 'mul',
        'con': 'add',
    },
    'v': {
        'ant': 'add',
        'con': 'mul',
    },
    '->': {
        'ant': 'add',
        'con': 'mul'
    }
}

RULES = {
    '~': {
        'ant': {
            'add': LNeg,
            'mul': LNeg
        },
        'con': {
            'add': RNeg,
            'mul': RNeg
        },
    },
    '&': {
        'ant': {
            'add': AddLAnd,
            'mul': MultLAnd
        },
        'con': {
            'add': AddRAnd,
            'mul': MultRAnd
        },
    },
    'v': {
        'ant': {
            'add': AddLOr,
            'mul': MultLOr
        },
        'con': {
            'add': AddROr,
            'mul': MultROr
        },
    },
    '->': {
        'ant': {
            'add': AddLIf,
            'mul': MultLIf
        },
        'con': {
            'add': AddRIf,
            'mul': MultRIf
        },
    }
}


def get_rule(proposition: Proposition, side: str, /, t=None) -> Rule:
    """
    Return the appropriate function for decomposing a proposition.

    :param proposition: A proposition object (atoms cause exceptions)
    :param side: Either 'ant' or 'con'
    :param t: Either None, 'mul', or 'add'
    """
    assert side in {'ant', 'con'}   
    if proposition.complexity < 1:
        raise Proposition.AtomicDecompositionError(proposition)
    connective = proposition.symb
    if t is None:
        t = DEFAULTS[connective][side]
    return RULES[connective][side][t]
    

