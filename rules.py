from enum import Enum, IntEnum
from typing import Protocol, TypeVar

from proposition import Proposition, Conjunction, Disjunction, Negation, Conditional
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
