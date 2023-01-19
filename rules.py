from enum import Enum
from typing import Protocol, TypeVar

from proposition import Proposition, Conjunction, Disjunction
from sequent import Sequent

decomp_result = TypeVar('decomp_result',
                        list[tuple[Sequent]],  # One-Parent Invertible
                        list[tuple[Sequent, Sequent]],  # Two-Parent Invertible
                        list[tuple[Sequent], ...],  # One-Parent Non-Invertible
                        list[tuple[Sequent, Sequent], ...]  # Two-Parent Non-Invertible
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

    def apply(self) -> list[tuple[Sequent]]:
        prop_sequent = Sequent(
            ant=(self.prop.left, self.prop.right),
            con=None
        )
        return [(self.sequent.mix(prop_sequent),)]


class RightMultOr:
    type = RuleTypes.OPI

    def __init__(self, prop: Disjunction, sequent: Sequent):
        self.prop = prop
        self.sequent = sequent

    def apply(self) -> list[tuple[Sequent]]:
        prop_sequent = Sequent(
            ant=None,
            con=(self.prop.left, self.prop.right)
        )
        return [(self.sequent.mix(prop_sequent),)]


class RightMultIf:
    type = RuleTypes.OPI

    def __init__(self, prop: Disjunction, sequent: Sequent):
        self.prop = prop
        self.sequent = sequent

    def apply(self) -> list[tuple[Sequent]]:
        prop_sequent = Sequent(
            ant=self.prop.left,
            con=self.prop.right
        )
        return [(self.sequent.mix(prop_sequent),)]