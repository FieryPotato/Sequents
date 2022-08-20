from abc import ABC, abstractmethod

from src.proposition import Proposition
from src.sequent import Sequent, Axiom


class Decomposer(ABC):
    """Abstract class for decomposer objects."""
    num_parents: int
    is_invertible: bool

    def __init__(self, sequent: Sequent, rule: Rule) -> None:
        self.sequent = sequent
        prop, side, index = sequent.first_complex_prop
        self.removed_main_prop = sequent.remove(side, index)
        self.rule = rule(self.prop)

    @abstractmethod
    def decompose(self) -> Any:
        """Apply self.rule to self.sequent."""

class DecomposeAtom(Decomposer):
    """Decomposer for atoms."""
    num_parents = 0
    is_invertible = True

    def decompose(self) -> Axiom:
        return Axiom()

class DecomposeInvertibleOneParent(Decomposer):
    """Decomposer for invertible single-parent rules."""
    num_parents = 1
    is_invertible = True

    def decompose(self) -> Sequent:
        rule_result = self.rule.apply()
        return Sequent.mix(self.removed_main_prop, rule_result)

class DecomposeInvertibleTwoParent(Decomposer):
    """Decomposer for invertible two-parent rules."""
    num_parents = 2
    is_invertible = True

    def decompose(self) -> tuple[Sequent]:
        rule_result = self.rule.apply()
        return (
            Sequent.mix(self.removed_main_prop, rule_result[0]),
            Sequent.mix(self.removed_main_prop, rule_result[1])
        )

class DecomposeNonInvertibleOneParent(Decomposer):
    """Decomposer for non-invertible single-parent rules."""
    num_parents = 1
    is_invertible = False

    def decompose(self) -> list[Sequent]:
        rule_result = self.rule.apply()
        return [
            Sequent.mix(self.removed_main_prop, rule_result[0]),
            Sequent.mix(self.removed_main_prop, rule_result[1])
        ]

class DecomposeNonInvertibleTwoParent(Decomposer):
    """Decomposer for non-invertible two-parent rules."""
    num_parentns = 2
    is_invertible = False

    def decompose(self) -> list[tuple[Sequent]]:
        rule_result = self.rule.apply()
        decomp_results = []
        for left, right in self.sequent.possible_mix_parents:
            l_result = Sequent.mix(left, rule_result)
            r_result = Sequent.mix(right, rule_result)
            decomp_results.append((l_result, r_result))
        return decomp_results

class Rule(ABC):
    """Abstract class for rules."""
    def __init__(self, proposition: Proposition) -> None:
        self.proposition = proposition

    @abstractmethod
    def apply(self) -> Sequent | tuple[Sequent]:
        """Apply this rule."""


class Atom(Rule):
    def decompose(self) -> None:
        return None


class LNeg(Rule):
    is_invertible = True
    num_parents = 1

    def decompose(self) -> Sequent:
        """Apply left negation rule to self.sequent."""
        return Sequent(tuple(), self.proposition.content)


class RNeg(Rule):
    is_invertible = True
    num_parents = 1

    def decompose(self) -> Sequent:
        """Apply right negation rule to self.sequent."""
        return Sequent(self.proposition.content, tuple())  

class MultLAnd(Rule):
    is_invertible = True
    num_parents = 1

    def decompose(self) -> Sequent:
        """Apply multiplicative left conjunction rule to self.sequent."""
        return Sequent(self.proposition.content, tuple())

class AddLAnd(Rule):
    is_invertible = False
    num_parents = 1

    def decompose(self) -> tuple[Sequent]:
        """Apply additive left conjunction rule to self.sequent."""
        pass
        #return (Sequent((self.proposition[0],), tuple(),
        #        Sequent(tuple(), (self.proposition[1],)))

class MultRAnd(Rule):
    is_invertible = False
    num_parents = 2

    def decompose(self) -> tuple[Sequent]:
        """Apply multiplicative right conjunction rule to self.sequent."""
        pass

class AddRAnd(Rule):
    is_invertible = True
    num_parents = 2

    def decompose(self) -> tuple[Sequent]:
        """Apply additive right conjunction rule to self.sequent."""
        return (
            Sequent(tuple(), (prop.left,)),
            Sequent(tuple(), (prop.right,))
        )

class MultLOr(Rule):
    is_invertible = False
    num_parents = 2

    def decompose(self) -> tuple[Sequent]:
        """Apply multiplicative left disjunction rule to self.sequent."""
        pass

class AddLOr(Rule):
    is_invertible = True
    num_parents = 2

    def decompose(self) -> tuple[Sequent]:
        """Apply additive left disjunction rule to self.sequent."""
        return (
            Sequent((prop.left,), tuple()),
            Sequent((prop.right,), tuple())
        )

class MultROr(Rule):
    is_invertible = True
    num_parents = 1

    def decompose(self) -> Sequent:
        """Apply multiplicative right disjunction rule to self.sequent."""
        return Sequent(tuple(), prop.content)

class AddROr(Rule):
    is_invertible = False
    num_parents = 1

    def decompose(self) -> tuple[Sequent]:
        """Apply additive right disjunction rule to self.sequent."""
        pass

class MultLIf(Rule):
    is_invertible = False
    num_parents = 2

    def decompose(self) -> tuple[Sequent]:
        """Apply multiplicative left conditional rule to self.sequent."""
        pass

class AddLIf(Rule):
    is_invertible = True
    num_parents = 2

    def decompose(self) -> tuple[Sequent]:
        """Apply additive left conditional rule to self.sequent."""
        return (
            Sequent(tuple(), (prop.left,)),
            Sequent((prop.right,), tuple())   
        )

class MultRIf(Rule): 
    is_invertible = True
    num_parents = 1

    def decompose(self) -> Sequent: 
        """Apply multiplicative right conditional rule to self.sequent.""" 
        return Sequent((prop.left,), (prop.right,))

class AddRIf(Rule):
    is_invertible = False
    num_parents = 1

    def decompose(self) -> tuple[Sequent]:
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
    rule = RULES[connective][side][t]
    return rule(proposition)
    

