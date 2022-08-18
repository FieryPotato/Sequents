from abc import ABC, abstractmethod

from src.proposition import Proposition
from src.sequent import Sequent


class Rule(ABC):
    """Abstract class for rules."""

    def __init__(self, sequent: Sequent) -> None:
        self.sequent = sequent

    @abstractmethod
    def apply(self) -> list[Sequent]:
        """Apply this rule to self.sequent."""

class LNeg(Rule):
    def apply(self) -> list[Sequent]:
        """Apply left negation rule to self.sequent."""
        pass

class RNeg(Rule):
    def apply(self) -> list[Sequent]:
        """Apply right negation rule to self.sequent."""
        pass

class MultLAnd(Rule):
    def apply(self) -> list[Sequent]:
        """Apply multiplicative left conjunction rule to self.sequent."""
        pass

class AddLAnd(Rule):
    def apply(self) -> list[Sequent]:
        """Apply additive left conjunction rule to self.sequent."""
        pass

class MultRAnd(Rule):
    def apply(self) -> list[Sequent]:
        """Apply multiplicative right conjunction rule to self.sequent."""
        pass

class AddRAnd(Rule):
    def apply(self) -> list[Sequent]:
        """Apply additive right conjunction rule to self.sequent."""
        pass

class MultLOr(Rule):
    def apply(self) -> list[Sequent]:
        """Apply multiplicative left disjunction rule to self.sequent."""
        pass

class AddLOr(Rule):
    def apply(self) -> list[Sequent]:
        """Apply additive left disjunction rule to self.sequent."""
        pass

class MultROr(Rule):
    def apply(self) -> list[Sequent]:
        """Apply multiplicative right disjunction rule to self.sequent."""
        pass

class AddROr(Rule):
    def apply(self) -> list[Sequent]:
        """Apply additive right disjunction rule to self.sequent."""
        pass

class MultLIf(Rule):
    def apply(self) -> list[Sequent]:
        """Apply multiplicative left conditional rule to self.sequent."""
        pass

class AddLIf(Rule):
    def apply(self) -> list[Sequent]:
        """Apply additive left conditional rule to self.sequent."""
        pass

class MultRIf(Rule):
    def apply(self) -> list[Sequent]:
        """Apply multiplicative right conditional rule to self.sequent."""
        pass

class AddRIf(Rule):
    def apply(self) -> list[Sequent]:
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
    """
    assert side in {'ant', 'con'}   
    if proposition.complexity < 1:
        raise Proposition.AtomicDecompositionError(proposition)
    connective = proposition.symb
    if t is None:
        t = DEFAULTS[connective][side]
    return RULES[connective][side][t]
    

