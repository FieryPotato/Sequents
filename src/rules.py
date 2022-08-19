from abc import ABC, abstractmethod

from src.proposition import Proposition
from src.sequent import Sequent


class Rule(ABC):
    """Abstract class for rules."""
    
    def __init__(self, sequent: Sequent) -> None:
        self.sequent = sequent
        self.prop, side, index = sequent.first_complex_prop
        self.main_prop_removed = sequent.remove(side, index)

    def apply(self) -> list:
        """
        Apply this rule to self.sequent and return the results as a dict.
        """
        # decomposed is a list of sequents for invertible rules
        # decomposed is a list of lists of sequents for non-invertible rules
        decomposed = self.decompose()
        return self.process(decomposed)

    @abstractmethod 
    def decompose(self) -> list[Sequent] | set[list[Sequent]]:
        """Return the results of applying this rule to self.sequent."""

    @abstractmethod
    def process(self, decomposed: list[Sequent] | list[list[Sequent]]) -> list:
        """Convert sequents resulting from decomposition into a dict."""


class InvertibleRule(Rule, ABC):
    """Abstract class for invertible rules."""
    is_invertible = True

    def process(self, decomposed: list[Sequent]) -> list[Sequent]:
        results = []
        for decomp_result in decomposed:
            new_sequent = Sequent.mix(decomp_result, self.main_prop_removed)
            results.append(new_sequent)
        return results


class NonInvertibleRule(Rule, ABC):
    """Abstract class for non-invertible rules."""
    is_invertible = False

    def process(self, decomposed: list[list[Sequent]]) -> list[Sequent]:
        


class LNeg(InvertibleRule):
    def decompose(self) -> list[Sequent]:
        """Apply left negation rule to self.sequent."""
        return [Sequent(tuple(), (prop.content[0],))]


class RNeg(InvertibleRule):
    def decompose(self) -> list[Sequent]:
        """Apply right negation rule to self.sequent."""
        return [Sequent((prop.content[0],), tuple())]        

class MultLAnd(InvertibleRule):
    def decompose(self) -> list[Sequent]:
        """Apply multiplicative left conjunction rule to self.sequent."""
        return [Sequent(prop.content, tuple())]

class AddLAnd(Rule):
    is_invertible = False
    def decompose(self) -> list[Sequent]:
        """Apply additive left conjunction rule to self.sequent."""
        pass

class MultRAnd(Rule):
    is_invertible = False
    def decompose(self) -> list[Sequent]:
        """Apply multiplicative right conjunction rule to self.sequent."""
        pass

class AddRAnd(InvertibleRule):
    def decompose(self) -> list[Sequent]:
        """Apply additive right conjunction rule to self.sequent."""
        return [
            Sequent(tuple(), (prop.left,)),
            Sequent(tuple(), (prop.right,))
        ]

class MultLOr(Rule):
    is_invertible = False
    def decompose(self) -> list[Sequent]:
        """Apply multiplicative left disjunction rule to self.sequent."""
        pass

class AddLOr(InvertibleRule):
    def decompose(self) -> list[Sequent]:
        """Apply additive left disjunction rule to self.sequent."""
        return [
            Sequent((prop.left,), tuple()),
            Sequent((prop.right,), tuple())
        ]

class MultROr(InvertibleRule):
    def decompose(self) -> list[Sequent]:
        """Apply multiplicative right disjunction rule to self.sequent."""
        return [Sequent(tuple(), prop.content)]

class AddROr(Rule):
    is_invertible = False
    def decompose(self) -> list[Sequent]:
        """Apply additive right disjunction rule to self.sequent."""
        pass

class MultLIf(Rule):
    is_invertible = False
    def decompose(self) -> list[Sequent]:
        """Apply multiplicative left conditional rule to self.sequent."""
        pass

class AddLIf(InvertibleRule):
    def decompose(self) -> list[Sequent]:
        """Apply additive left conditional rule to self.sequent."""
        return [
            Sequent(tuple(), (prop.left,)),
            Sequent((prop.right,), tuple())   
        ] 

class MultRIf(InvertibleRule): 
    is_invertible = True
    def decompose(self) -> list[Sequent]: 
        """Apply multiplicative right conditional rule to self.sequent.""" 
        return [Sequent((prop.left,), (prop.right,))]

class AddRIf(Rule):
    is_invertible = False
    def decompose(self) -> list[Sequent]:
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
    

