from typing import Protocol, TypeVar

from proposition import Proposition, Conjunction, Disjunction, Negation, Conditional, Quantifier, Universal, Existential
from sequent import Sequent
from settings import Settings

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
        self.proposition = proposition
        self.sequent = sequent
        self.names = names

    def apply(self) -> tuple[tuple[Sequent], ...]:
        prop_sequents = (
            Sequent(
                ant=self.proposition.instantiate_with(name),
                con=None
            )
            for name in self.names
        )
        return tuple((self.sequent.mix(sequent),) for sequent in prop_sequents)  # type: ignore


class RightForall:
    invertible = False
    parents = 1

    def __init__(self, proposition: Universal, sequent: Sequent, names: set[str]):
        # Right Universals can only be instantiated by names not present
        # in the rest of the sequent
        legal_names: set[str] = names - proposition.names.union(sequent.names)
        if not legal_names:
            legal_names.add('NONE')
        self.proposition = proposition
        self.sequent = sequent
        self.names = legal_names

    def apply(self) -> tuple[tuple[Sequent], ...]:
        prop_sequents = (
            Sequent(
                ant=None,
                con=self.proposition.instantiate_with(name),
            )
            for name in self.names
        )
        return tuple((self.sequent.mix(sequent),) for sequent in prop_sequents)  # type: ignore


class LeftExists:
    invertible = False
    parents = 1

    def __init__(self, proposition: Existential, sequent: Sequent, names: set[str]):
        if not names:
            names.add('NONE')
        self.proposition = proposition
        self.sequent = sequent
        self.names = names

    def apply(self) -> tuple[tuple[Sequent], ...]:
        prop_sequents = (
            Sequent(
                ant=self.proposition.instantiate_with(name),
                con=None,
            )
            for name in self.names
        )
        return tuple((self.sequent.mix(sequent),) for sequent in prop_sequents)


class RightExists:
    invertible = False
    parents = 1

    def __init__(self, proposition: Existential, sequent: Sequent, names: set[str]):
        if not names:
            names.add('NONE')
        self.proposition = proposition
        self.sequent = sequent
        self.names = names

    def apply(self) -> tuple[tuple[Sequent], ...]:
        prop_sequents = (
            Sequent(
                ant=None,
                con=self.proposition.instantiate_with(name)
            )
            for name in self.names
        )
        return tuple((self.sequent.mix(sequent),) for sequent in prop_sequents)


RULE_DICT = {
    'ant': {
        '~': {'add': LeftNot,
              'mul': LeftNot},
        '&': {'add': ...,
              'mul': LeftMultAnd},
        'v': {'add': LeftAddOr,
              'mul': ...},
        '->': {'add': LeftAddIf,
               'mul': ...},
        '∀': {'add': LeftForall,
              'mul': LeftForall},
        '∃': {'add': LeftExists,
              'mul': LeftExists},
    },
    'con': {
        '~': {'add': RightNot,
              'mul': RightNot},
        '&': {'add': RightAddAnd,
              'mul': ...},
        'v': {'add': ...,
              'mul': RightMultOr},
        '->': {'add': ...,
               'mul': RightMultIf},
        '∀': {'add': RightForall,
              'mul': RightForall},
        '∃': {'add': RightExists,
              'mul': RightExists},
    }
}


def get_rule(sequent: Sequent, names: set[str] = None) -> Rule:
    prop, side, index = sequent.first_complex_prop()
    sequent_minus_prop = sequent.remove_proposition_at(side, index)
    rule_type = Settings().get_rule(connective=prop.symb, side=side)
    rule = RULE_DICT[side][prop.symb][rule_type]
    if isinstance(prop, Quantifier):
        return rule(prop, sequent_minus_prop, names)
    return rule(prop, sequent_minus_prop)
