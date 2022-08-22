import json
from abc import ABC, abstractmethod
from typing import Any

from proposition import Proposition
from sequent import Sequent

CONFIG_FILE = 'config.json'


class Decomposer(ABC):
    """Abstract class for decomposer objects."""
    num_parents: int
    is_invertible: bool

    def __init__(self, sequent: Sequent = None) -> None:
        self.sequent = sequent
        prop, side, index = sequent.first_complex_prop
        self.removed_main_prop = sequent.remove(side, index)
        self.rule = get_rule(prop, side)


    @abstractmethod
    def decompose(self) -> Any:
        """Apply self.rule to self.sequent."""
        
    @abstractmethod
    def get_parents(self) -> dict | list | None:
        """Return self.sequent's parents as a dict for tree branches.""" 


class DecomposeAtom(Decomposer):
    """Decomposer for axioms."""
    def __init__(self, sequent=Sequent) -> None:
        self.sequent = sequent
        self.rule = Axiom()

    def decompose(self) -> None:
        return self.rule.apply()

    def get_parents(self) -> None:
        return None

class DecomposeInvertibleOneParent(Decomposer):
    """Decomposer for invertible single-parent rules."""
    num_parents = 1
    is_invertible = True

    def decompose(self) -> Sequent | None:
        rule_result = self.rule.apply()
        # todo: move this check and return none out
        if rule_result is not None:
            return Sequent.mix(self.removed_main_prop, rule_result)
        return None
        
    def get_parents(self) -> dict:
        parent = self.decompose()
        return {parent: {}}


class DecomposeInvertibleTwoParent(Decomposer):
    """Decomposer for invertible two-parent rules."""
    num_parents = 2
    is_invertible = True

    def decompose(self) -> tuple[Sequent, Sequent]:
        rule_result = self.rule.apply()
        return (
            Sequent.mix(self.removed_main_prop, rule_result[0]),
            Sequent.mix(self.removed_main_prop, rule_result[1])
        )
        
    def get_parents(self) -> dict: 
        left, right = self.decompose()
        return {
            left: {},
            right: {}
        } 


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
    
    def get_parents(self) -> list:
        a, b = self.decompose()
        return [
                a: {},
                b: {}
        ]


class DecomposeNonInvertibleTwoParent(Decomposer):
    """Decomposer for non-invertible two-parent rules."""
    num_parents = 2
    is_invertible = False

    def decompose(self) -> list[tuple[Sequent, Sequent]]:
        rule_result = self.rule.apply()

        decomp_results = []
        for left, right in self.removed_main_prop.possible_mix_parents:
            l_result = Sequent.mix(left, rule_result[0])
            r_result = Sequent.mix(right, rule_result[1])
            decomp_results.append((l_result, r_result))
        return decomp_results

    def get_parents(self) -> dict:
        decomp_results = self.decompose()
        parents = []
        for left, right in results:
            sub_dict = {
                left: {},
                right: {}
            }
            parents.append(sub_dict) 
        return parents 

class Rule(ABC):
    """Abstract class for rules."""

    def __init__(self, proposition: Proposition = None) -> None:
        self.proposition = proposition

    @abstractmethod
    def apply(self) -> Sequent | tuple[Sequent]:
        """Apply this rule."""


class Axiom(Rule):
    def apply(self) -> None:
        return None


class LNeg(Rule):
    is_invertible = True
    num_parents = 1

    def apply(self) -> Sequent:
        """Apply left negation rule to self.sequent."""
        return Sequent((), self.proposition.content)


class RNeg(Rule):
    is_invertible = True
    num_parents = 1

    def apply(self) -> Sequent:
        """Apply right negation rule to self.sequent."""
        return Sequent(self.proposition.content, ())


class MultLAnd(Rule):
    is_invertible = True
    num_parents = 1

    def apply(self) -> Sequent:
        """Apply multiplicative left conjunction rule to self.sequent."""
        return Sequent(self.proposition.content, ())


class AddLAnd(Rule):
    is_invertible = False
    num_parents = 1

    def apply(self) -> tuple[Sequent, Sequent]:
        """Apply additive left conjunction rule to self.sequent."""
        return (Sequent((self.proposition.left,), ()),
                Sequent((self.proposition.right,), ()))


class MultRAnd(Rule):
    is_invertible = False
    num_parents = 2

    def apply(self) -> tuple[Sequent, Sequent]:
        """Apply multiplicative right conjunction rule to self.sequent."""
        return (
            Sequent((), (self.proposition.left,)),
            Sequent((), (self.proposition.right,))
        )


class AddRAnd(Rule):
    is_invertible = True
    num_parents = 2

    def apply(self) -> tuple[Sequent, Sequent]:
        """Apply additive right conjunction rule to self.sequent."""
        return (
            Sequent((), (self.proposition.left,)),
            Sequent((), (self.proposition.right,))
        )


class MultLOr(Rule):
    is_invertible = False
    num_parents = 2

    def apply(self) -> tuple[Sequent, Sequent]:
        """Apply multiplicative left disjunction rule to self.sequent."""
        return (
            Sequent((self.proposition.left,), ()),
            Sequent((self.proposition.right,), ())
        )


class AddLOr(Rule):
    is_invertible = True
    num_parents = 2

    def apply(self) -> tuple[Sequent, Sequent]:
        """Apply additive left disjunction rule to self.sequent."""
        return (
            Sequent((self.proposition.left,), ()),
            Sequent((self.proposition.right,), ())
        )


class MultROr(Rule):
    is_invertible = True
    num_parents = 1

    def apply(self) -> Sequent:
        """Apply multiplicative right disjunction rule to self.sequent."""
        return Sequent((), self.proposition.content)


class AddROr(Rule):
    is_invertible = False
    num_parents = 1

    def apply(self) -> tuple[Sequent, Sequent]:
        """Apply additive right disjunction rule to self.sequent."""
        return (
            Sequent((), (self.proposition.left,)),
            Sequent((), (self.proposition.right,))
        )


class MultLIf(Rule):
    is_invertible = False
    num_parents = 2

    def apply(self) -> tuple[Sequent, Sequent]:
        """Apply multiplicative left conditional rule to self.sequent."""
        return (
            Sequent((), (self.proposition.left,)),
            Sequent((self.proposition.right,), ())
        )


class AddLIf(Rule):
    is_invertible = True
    num_parents = 2

    def apply(self) -> tuple[Sequent, Sequent]:
        """Apply additive left conditional rule to self.sequent."""
        return (
            Sequent((), (self.proposition.left,)),
            Sequent((self.proposition.right,), ())
        )


class MultRIf(Rule):
    is_invertible = True
    num_parents = 1

    def apply(self) -> Sequent:
        """Apply multiplicative right conditional rule to self.sequent."""
        return Sequent((self.proposition.left,), (self.proposition.right,))


class AddRIf(Rule):
    is_invertible = False
    num_parents = 1

    def apply(self) -> tuple[Sequent, Sequent]:
        """Apply additive right conditional rule to self.sequent."""
        return (
            Sequent((self.proposition.left,), ()),
            Sequent((), (self.proposition.right,))
        )


rules = {
    '~': {'ant': {
        'add': LNeg,
        'mul': LNeg
    }, 'con': {
        'add': RNeg,
        'mul': RNeg
    }, },
    '&': {'ant': {
        'add': AddLAnd,
        'mul': MultLAnd
    }, 'con': {
        'add': AddRAnd,
        'mul': MultRAnd
    }, },
    'v': {'ant': {
        'add': AddLOr,
        'mul': MultLOr
    }, 'con': {
        'add': AddROr,
        'mul': MultROr
    }, },
    '->': {'ant': {
        'add': AddLIf,
        'mul': MultLIf
    }, 'con': {
        'add': AddRIf,
        'mul': MultRIf
    }, }
}

decomposers = {
    '~': {'ant': {
        'add': DecomposeInvertibleOneParent,
        'mul': DecomposeInvertibleOneParent
    }, 'con': {
        'add': DecomposeInvertibleOneParent,
        'mul': DecomposeInvertibleOneParent
    }, },
    '&': {'ant': {
        'add': DecomposeNonInvertibleOneParent,
        'mul': DecomposeInvertibleOneParent
    }, 'con': {
        'add': DecomposeInvertibleTwoParent,
        'mul': DecomposeNonInvertibleTwoParent
    }, },
    'v': {'ant': {
        'add': DecomposeInvertibleTwoParent,
        'mul': DecomposeNonInvertibleTwoParent
    }, 'con': {
        'add': DecomposeNonInvertibleOneParent,
        'mul': DecomposeInvertibleOneParent
    }, },
    '->': {'ant': {
        'add': DecomposeInvertibleTwoParent,
        'mul': DecomposeNonInvertibleTwoParent
    }, 'con': {
        'add': DecomposeNonInvertibleOneParent,
        'mul': DecomposeInvertibleOneParent
    }, }
}

rule_settings = {}


def load_rule_settings() -> None:
    """Initialize global rule_settings variable."""
    global rule_settings

    with open(CONFIG_FILE, 'r') as file:
        settings = json.load(file)
    rule_settings = settings['connective_type']


def get_rule_setting(connective, side) -> str:
    if not rule_settings:
        load_rule_settings()
    return rule_settings[connective][side]


def get_rule(proposition: Proposition, side: str) -> Rule:
    """
    Return the appropriate function for decomposing a proposition.

    :param proposition: A proposition object (atoms cause exceptions)
    :param side: Either 'ant' or 'con'
    """
    connective = proposition.symb
    if not connective:
        return Axiom(proposition)
    decomp_type = get_rule_setting(connective, side)
    rule = rules[connective][side][decomp_type]
    return rule(proposition)


def get_decomposer(sequent: Sequent) -> Decomposer:
    """Return the appropriate decomposer for a given sequent."""
    if sequent.is_atomic:
        return DecomposeAtom(sequent)
    prop, side, index = sequent.first_complex_prop
    connective = prop.symb
    decomp_type = get_rule_setting(connective, side)
    decomposer = decomposers[connective][side][decomp_type]
    return decomposer(sequent)
