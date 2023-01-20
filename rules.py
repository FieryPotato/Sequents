from typing import Protocol, TypeVar

from proposition import Proposition, Conjunction, Disjunction, Negation, Conditional, Quantifier, Universal
from sequent import Sequent

decomp_result = TypeVar('decomp_result',
                        tuple[tuple[Sequent]],  # One-Parent Invertible
                        tuple[tuple[Sequent, Sequent]],  # Two-Parent Invertible
                        tuple[tuple[Sequent], ...],  # One-Parent Non-Invertible
                        tuple[tuple[Sequent, Sequent], ...]  # Two-Parent Non-Invertible
                        )


class Rule(Protocol):
    invertible: bool
    parents: int
    proposition: Proposition
    sequent: Sequent

    def apply(self) -> decomp_result:
        ...


class LeftMultAnd:
    invertible = True
    parents = 1

    def __init__(self, proposition: Conjunction, sequent: Sequent):
        self.proposition = proposition
        self.sequent = sequent

    def apply(self) -> tuple[tuple[Sequent]]:
        prop_sequent = Sequent(
            ant=(self.proposition.left, self.proposition.right),
            con=None
        )
        return (self.sequent.mix(prop_sequent),),


class RightAddAnd:
    invertible = True
    parents = 2
    
    def __init__(self, proposition: Conjunction, sequent: Sequent):
        self.proposition = proposition
        self.sequent = sequent
    
    def apply(self) -> tuple[tuple[Sequent, Sequent]]:
        left = Sequent(
            ant=None,
            con=self.proposition.left
        )
        right = Sequent(
            ant=None,
            con=self.proposition.right
        )
        return tuple(self.sequent.mix(parent) for parent in (left, right)),  # type: ignore


class RightMultOr:
    invertible = True
    parents = 1

    def __init__(self, proposition: Disjunction, sequent: Sequent):
        self.proposition = proposition
        self.sequent = sequent

    def apply(self) -> tuple[tuple[Sequent]]:
        prop_sequent = Sequent(
            ant=None,
            con=(self.proposition.left, self.proposition.right)
        )
        return (self.sequent.mix(prop_sequent),),


class LeftAddOr:
    invertible = True
    parents = 2
    
    def __init__(self, proposition: Disjunction, sequent: Sequent):
        self.proposition = proposition
        self.sequent = sequent
        
    def apply(self) -> tuple[tuple[Sequent, Sequent]]:
        left = Sequent(
            ant=self.proposition.left,
            con=None
        )
        right = Sequent(
            ant=self.proposition.right,
            con=None
        )
        return tuple(self.sequent.mix(parent) for parent in (left, right)),  # type: ignore


class RightMultIf:
    invertible = True
    parents = 1

    def __init__(self, proposition: Conditional, sequent: Sequent):
        self.proposition = proposition
        self.sequent = sequent

    def apply(self) -> tuple[tuple[Sequent]]:
        prop_sequent = Sequent(
            ant=self.proposition.left,
            con=self.proposition.right
        )
        return (self.sequent.mix(prop_sequent),),


class LeftAddIf:
    invertible = True
    parents = 2
    
    def __init__(self, proposition: Conditional, sequent: Sequent):
        self.proposition = proposition
        self.sequent = sequent
        
    def apply(self) -> tuple[tuple[Sequent, Sequent]]:
        left = Sequent(
            ant=None,
            con=self.proposition.left
        )
        right = Sequent(
            ant=self.proposition.right,
            con=None
        )
        return tuple(self.sequent.mix(parent) for parent in (left, right)),  # type: ignore

class LeftNot:
    invertible = True
    parents = 1

    def __init__(self, proposition: Negation, sequent: Sequent):
        self.proposition = proposition
        self.sequent = sequent

    def apply(self) -> tuple[tuple[Sequent]]:
        prop_sequent = Sequent(
            ant=None,
            con=self.proposition.prop
        )
        return (self.sequent.mix(prop_sequent),),


class RightNot:
    invertible = True
    parents = 1

    def __init__(self, proposition: Negation, sequent: Sequent):
        self.proposition = proposition
        self.sequent = sequent

    def apply(self) -> tuple[tuple[Sequent]]:
        prop_sequent = Sequent(
            ant=self.proposition.prop,
            con=None
        )
        return (self.sequent.mix(prop_sequent),),


class LeftForall:
    invertible = False
    parents = 1

    def __init__(self, proposition: Universal, sequent: Sequent, names: set[str]):
        if not names:
            names.add('NONE')
        self.names = names
        self.proposition = proposition
        self.sequent = sequent

    def apply(self) -> tuple[tuple[Sequent], ...]:
        prop_sequents = (
            Sequent(
                ant=self.proposition.instantiate_with(name),
                con=None
            )
            for name in self.names
        )
        return tuple((self.sequent.mix(sequent),) for sequent in prop_sequents)  # type: ignore


RULE_DICT = {
    'ant': {
        '~': LeftNot,
        '&': LeftMultAnd,
        'v': LeftAddOr,
        '->': LeftAddIf,
        '∀': LeftForall,
        '∃': ...,
    },
    'con': {
        '~': RightNot,
        '&': RightAddAnd,
        'v': RightMultOr,
        '->': RightMultIf,
        '∀': ...,
        '∃': ...,
    }
}


def get_rule(sequent: Sequent, names: set[str] = None) -> Rule:
    prop, side, index = sequent.first_complex_prop()
    sequent_minus_prop = sequent.remove_proposition_at(side, index)
    rule = RULE_DICT[side][prop.symb]
    if isinstance(prop, Quantifier):
        return rule(prop, sequent_minus_prop, names)
    return rule(prop, sequent_minus_prop)