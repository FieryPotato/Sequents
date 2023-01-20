from enum import Enum
from typing import Protocol, TypeVar

from proposition import Proposition, Conjunction, Disjunction, Negation, Conditional
from sequent import Sequent

decomp_result = TypeVar('decomp_result',
                        tuple[tuple[Sequent]],  # One-Parent Invertible
                        tuple[tuple[Sequent, Sequent]],  # Two-Parent Invertible
                        tuple[tuple[Sequent], ...],  # One-Parent Non-Invertible
                        tuple[tuple[Sequent, Sequent], ...]  # Two-Parent Non-Invertible
                        )


class RuleTypes(Enum):
    OPI = 'One-Parent Invertible'
    TPI = 'Two-Parent Invertible'
    OPNI = 'One-Parent Non-Invertible'
    TPNI = 'Two-Parent Non-Invertible'


class Rule(Protocol):
    type: RuleTypes
    prop: Proposition
    sequent: Sequent

    def apply(self) -> decomp_result:
        ...


class LeftMultAnd:
    type = RuleTypes.OPI

    def __init__(self, prop: Conjunction, sequent: Sequent):
        self.prop = prop
        self.sequent = sequent

    def apply(self) -> tuple[tuple[Sequent]]:
        prop_sequent = Sequent(
            ant=(self.prop.left, self.prop.right),
            con=None
        )
        return ((self.sequent.mix(prop_sequent),),)


class RightAddAnd:
    type = RuleTypes.TPI
    
    def __init__(self, prop: Conjunction, sequent: Sequent):
        self.prop = prop
        self.sequent = sequent
    
    def apply(self) -> tuple[tuple[Sequent, Sequent]]:
        left = Sequent(
            ant=None,
            con=self.prop.left
        )
        right = Sequent(
            ant=None,
            con=self.prop.right
        )
        return (
            tuple(
                self.sequent.mix(parent)
                for parent in left, right
            ),
        )

class RightMultOr:
    type = RuleTypes.OPI

    def __init__(self, prop: Disjunction, sequent: Sequent):
        self.prop = prop
        self.sequent = sequent

    def apply(self) -> tuple[tuple[Sequent]]:
        prop_sequent = Sequent(
            ant=None,
            con=(self.prop.left, self.prop.right)
        )
        return ((self.sequent.mix(prop_sequent),),)


class LeftAddOr:
    type = RuleTypes.TPI
    
    def __init__(self, prop: Disjunction, sequent: Sequent):
        self.prop = prop
        self.sequent = sequent
        
    def apply(self) -> tuple[tuple[Sequent, Sequent]]:
        left = Sequent(
            ant=self.prop.left,
            con=None
        )
        right = Sequent(
            ant=self.prop.right,
            con=None
        )
        return (
            tuple(
                self.sequent.mix(parent) 
                for parent in left, right
            ),
        )


class RightMultIf:
    type = RuleTypes.OPI

    def __init__(self, prop: Conditional, sequent: Sequent):
        self.prop = prop
        self.sequent = sequent

    def apply(self) -> tuple[tuple[Sequent]]:
        prop_sequent = Sequent(
            ant=self.prop.left,
            con=self.prop.right
        )
        return ((self.sequent.mix(prop_sequent),),)


class LeftAddIf:
    type = RuleTypes.TPI
    
    def __init__(self, prop: Conditional, sequent: Sequent):
        self.prop = prop
        self.sequent = sequent
        
    def apply(self) -> tuple[tuple[Sequent, Sequent]]:
        left = Sequent(
            ant=None,
            con=self.prop.left
        )
        right = Sequent(
            ant=self.prop.right,
            con=None
        )
        return (
            tuple(
                self.sequent.mix(parent) 
                for parent in left, right
            )
        )


class LeftNot:
    type = RuleTypes.OPI

    def __init__(self, prop: Negation, sequent: Sequent):
        self.prop = prop
        self.sequent = sequent

    def apply(self) -> tuple[tuple[Sequent]]:
        prop_sequent = Sequent(
            ant=None,
            con=self.prop.prop
        )
        return ((self.sequent.mix(prop_sequent),),)


class RightNot:
    type = RuleTypes.OPI

    def __init__(self, prop: Negation, sequent: Sequent):
        self.prop = prop
        self.sequent = sequent

    def apply(self) -> tuple[tuple[Sequent]]:
        prop_sequent = Sequent(
            ant=self.prop.prop,
            con=None
        )
        return ((self.sequent.mix(prop_sequent),),)
