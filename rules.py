from typing import Protocol, TypeVar

from proposition import Proposition, Conjunction, Disjunction, Negation, \
    Conditional, Quantifier, Universal, Existential
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


class LeftAddAnd:
    invertible = False
    parents = 1

    def __init__(self, proposition: Conjunction, sequent: Sequent):
        self.proposition = proposition
        self.sequent = sequent

    def apply(self) -> tuple[tuple[Sequent], ...]:
        parents = (
            Sequent(ant=prop, con=None)
            for prop in (self.proposition.left, self.proposition.right)
        )
        return tuple((self.sequent.mix(parent),) for parent in parents)


class RightAddAnd:
    invertible = True
    parents = 2

    def __init__(self, proposition: Conjunction, sequent: Sequent):
        self.proposition = proposition
        self.sequent = sequent

    def apply(self) -> tuple[tuple[Sequent, Sequent]]:
        left = Sequent(ant=None, con=self.proposition.left)
        right = Sequent(ant=None, con=self.proposition.right)
        return tuple(self.sequent.mix(parent) for parent in (left, right)),  # type: ignore


class RightMultAnd:
    invertible = False
    parents = 2

    def __init__(self, proposition: Conjunction, sequent: Sequent) -> None:
        self.proposition = proposition
        self.sequent = sequent

    def apply(self) -> tuple[tuple[Sequent, Sequent], ...]:
        left_parent = Sequent(ant=None, con=self.proposition.left)
        right_parent = Sequent(ant=None, con=self.proposition.right)
        results = (
            (left_parent.mix(left), right_parent.mix(right))
            for left, right in self.sequent.possible_mix_parents()
        )
        if not results:
            return tuple((left_parent, right_parent)),
        return tuple(results)


class RightMultOr:
    invertible = True
    parents = 1

    def __init__(self, proposition: Disjunction, sequent: Sequent):
        self.proposition = proposition
        self.sequent = sequent

    def apply(self) -> tuple[tuple[Sequent]]:
        prop_sequent = Sequent(ant=None, con=(self.proposition.left, self.proposition.right))
        return (self.sequent.mix(prop_sequent),),


class RightAddOr:
    invertible = True
    parents = 1

    def __init__(self, proposition: Disjunction, sequent: Sequent):
        self.proposition = proposition
        self.sequent = sequent

    def apply(self) -> tuple[tuple[Sequent], ...]:
        parents = (
            Sequent(ant=None, con=prop)
            for prop in (self.proposition.left, self.proposition.right)
        )
        return tuple((self.sequent.mix(parent),) for parent in parents)


class LeftAddOr:
    invertible = True
    parents = 2

    def __init__(self, proposition: Disjunction, sequent: Sequent):
        self.proposition = proposition
        self.sequent = sequent

    def apply(self) -> tuple[tuple[Sequent, Sequent]]:
        left = Sequent(ant=self.proposition.left, con=None)
        right = Sequent(ant=self.proposition.right, con=None)
        return tuple(self.sequent.mix(parent) for parent in (left, right)),  # type: ignore


class LeftMultOr:
    invertible = False
    parents = 2

    def __init__(self, proposition: Disjunction, sequent: Sequent) -> None:
        self.proposition = proposition
        self.sequent = sequent

    def apply(self) -> tuple[tuple[Sequent, Sequent], ...]:
        left_parent = Sequent(ant=self.proposition.left, con=None)
        right_parent = Sequent(ant=self.proposition.right, con=None)
        results = (
            (left_parent.mix(left), right_parent.mix(right))
            for left, right in self.sequent.possible_mix_parents()
        )
        if not results:
            return tuple((left_parent, right_parent)),
        return tuple(results)


class RightMultIf:
    invertible = True
    parents = 1

    def __init__(self, proposition: Conditional, sequent: Sequent):
        self.proposition = proposition
        self.sequent = sequent

    def apply(self) -> tuple[tuple[Sequent]]:
        prop_sequent = Sequent(ant=self.proposition.left, con=self.proposition.right)
        return (self.sequent.mix(prop_sequent),),


class RightAddIf:
    invertible = False
    parents = 1

    def __init__(self, proposition: Conditional, sequent: Sequent) -> None:
        self.proposition = proposition
        self.sequent = sequent

    def apply(self) -> tuple[tuple[Sequent], ...]:
        left_parent = Sequent(ant=None, con=self.proposition.left)
        right_parent = Sequent(ant=self.proposition.right, con=None)
        return tuple((self.sequent.mix(parent),) for parent in (left_parent, right_parent))


class LeftAddIf:
    invertible = True
    parents = 2

    def __init__(self, proposition: Conditional, sequent: Sequent):
        self.proposition = proposition
        self.sequent = sequent

    def apply(self) -> tuple[tuple[Sequent, Sequent]]:
        left = Sequent(ant=None, con=self.proposition.left)
        right = Sequent(ant=self.proposition.right, con=None)
        return tuple(self.sequent.mix(parent) for parent in (left, right)),  # type: ignore


class LeftMultIf:
    invertible = False
    parents = 2

    def __init__(self, proposition: Conditional, sequent: Sequent) -> None:
        self.proposition = proposition
        self.sequent = sequent

    def apply(self) -> tuple[tuple[Sequent, Sequent], ...]:
        left_parent = Sequent(ant=None, con=self.proposition.left)
        right_parent = Sequent(ant=self.proposition.right, con=None)
        results = (
            (left_parent.mix(left), right_parent.mix(right))
            for left, right in self.sequent.possible_mix_parents()
        )
        if not results:
            return tuple((left_parent, right_parent)),
        return tuple(results)


class LeftNot:
    invertible = True
    parents = 1

    def __init__(self, proposition: Negation, sequent: Sequent):
        self.proposition = proposition
        self.sequent = sequent

    def apply(self) -> tuple[tuple[Sequent]]:
        prop_sequent = Sequent(ant=None, con=self.proposition.prop)
        return (self.sequent.mix(prop_sequent),),


class RightNot:
    invertible = True
    parents = 1

    def __init__(self, proposition: Negation, sequent: Sequent):
        self.proposition = proposition
        self.sequent = sequent

    def apply(self) -> tuple[tuple[Sequent]]:
        prop_sequent = Sequent(ant=self.proposition.prop, con=None)
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
            Sequent(ant=self.proposition.instantiate_with(name), con=None)
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
            Sequent(ant=None, con=self.proposition.instantiate_with(name))
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
            Sequent(ant=self.proposition.instantiate_with(name), con=None)
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
            Sequent(ant=None, con=self.proposition.instantiate_with(name))
            for name in self.names
        )
        return tuple((self.sequent.mix(sequent),) for sequent in prop_sequents)


RULE_DICT = {
    'ant': {
        '~': {'add': LeftNot,
              'mul': LeftNot},
        '&': {'add': LeftAddAnd,
              'mul': LeftMultAnd},
        'v': {'add': LeftAddOr,
              'mul': LeftMultOr},
        '->': {'add': LeftAddIf,
               'mul': LeftMultIf},
        '∀': {'add': LeftForall,
              'mul': LeftForall},
        '∃': {'add': LeftExists,
              'mul': LeftExists},
    },
    'con': {
        '~': {'add': RightNot,
              'mul': RightNot},
        '&': {'add': RightAddAnd,
              'mul': RightMultAnd},
        'v': {'add': RightAddOr,
              'mul': RightMultOr},
        '->': {'add': RightAddIf,
               'mul': RightMultIf},
        '∀': {'add': RightForall,
              'mul': RightForall},
        '∃': {'add': RightExists,
              'mul': RightExists},
    }
}


def get_rule(sequent: Sequent, names: set[str] = None) -> Rule:
    """
    Return an object following the Rule protocol based on sequent. Rules
    are either invertible or not and have either 1 or 2 parents.

    Rule.proposition is the Proposition that will be decomposed.
    Rule.sequent is the Sequent from which the proposition came, minus
    that Proposition.

    Rule.apply() returns a tuple of tuples of Sequents representing the
    decomposition results as follows:
        - One-parent invertible -> tuple[tuple[Sequent]]
        - Two-parent invertible -> tuple[tuple[Sequent, Sequent]]
        - One-parent non-invertible -> tuple[tuple[Sequent], ...]
        - Two-parent non-invertible -> tuple[tuple[Sequent, Sequent], ...]

    """
    prop, side, index = sequent.first_complex_prop()
    sequent_minus_prop = sequent.remove_proposition_at(side, index)
    rule_type = Settings().get_rule(connective=prop.symb, side=side)
    rule = RULE_DICT[side][prop.symb][rule_type]
    if isinstance(prop, Quantifier):
        return rule(prop, sequent_minus_prop, names)
    return rule(prop, sequent_minus_prop)
