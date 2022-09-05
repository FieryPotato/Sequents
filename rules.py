"""
Module containing classes related to decomposing sequents. 

There are three distinctions in how propositions are decomposed 
(additive vs. multiplicative, invertible vs. non-invertible, and 
one-parent vs. two-parent) each of which is represented in an 
extensible way below.

Each connective has four Rule classes associated with it, accounting for
their left and right rules, as well as whether they're additive or 
multiplicative. These rule classes have one required method, apply(),
which returns one or more sequents containing the result of decomposing
that proposition. 

These rules are applied by the decomposers and mixed into parent 
sequents, with .decompose()'s return value being all sequents arising
from the decomposition of the initial sequent. 

The only function you should need to use, and which is only used in the
development of trees, is get_decomposer, which returns the decomposer 
object specific to its input sequent (accounting for the rules settings
in config.json.
"""

__all__ = ['get_decomposer']

from typing import Any, Protocol

from sequent import Sequent
from settings import Settings


class Proposition(Protocol):
    ...


class Decomposer(Protocol):
    """Protocol for decomposer objects."""
    num_parents: int
    is_invertible: bool

    def get_parents(self) -> dict | list | None:
        ...

class AtomDecomposer:
    """Decomposer for axioms."""
    num_parents: 0
    is_invertible: True

    def __init__(self, sequent: Sequent) -> None:
        self.sequent = sequent
        self.rule = Axiom()

    def get_parents(self) -> None:
        return None


class InvertibleOneParentDecomposer:
    """Decomposer for invertible single-parent rules."""
    num_parents = 1
    is_invertible = True

    def __init__(self, sequent: Sequent) -> None:
        self.sequent = sequent
        prop, side, index = sequent.first_complex_prop()
        self.removed_main_prop = sequent.remove(side, index)
        self.rule = get_rule(prop, side)

    def decompose(self) -> Sequent | None:
        rule_result = self.rule.apply()
        if rule_result is not None:
            return Sequent.mix(self.removed_main_prop, rule_result)
        return None

    def get_parents(self) -> dict:
        parent = self.decompose()
        return {parent: None}


class InvertibleTwoParentDecomposer:
    """Decomposer for invertible two-parent rules."""
    num_parents = 2
    is_invertible = True

    def __init__(self, sequent: Sequent) -> None:
        self.sequent = sequent
        prop, side, index = sequent.first_complex_prop()
        self.removed_main_prop = sequent.remove(side, index)
        self.rule = get_rule(prop, side)

    def decompose(self) -> tuple[Sequent, Sequent]:
        rule_result = self.rule.apply()
        return (
            Sequent.mix(self.removed_main_prop, rule_result[0]),
            Sequent.mix(self.removed_main_prop, rule_result[1])
        )

    def get_parents(self) -> dict:
        left, right = self.decompose()
        return {
            left: None,
            right: None
        }


class NonInvertibleOneParentDecomposer:
    """Decomposer for non-invertible single-parent rules."""
    num_parents = 1
    is_invertible = False

    def __init__(self, sequent: Sequent) -> None:
        self.sequent = sequent
        prop, side, index = sequent.first_complex_prop()
        self.removed_main_prop = sequent.remove(side, index)
        self.rule = get_rule(prop, side)

    def decompose(self) -> list[Sequent]:
        rule_result = self.rule.apply()
        return [
            Sequent.mix(self.removed_main_prop, rule_result[0]),
            Sequent.mix(self.removed_main_prop, rule_result[1])
        ]

    def get_parents(self) -> list:
        a, b = self.decompose()
        return [
            {a: None},
            {b: None}
        ]


class NonInvertibleTwoParentDecomposer:
    """Decomposer for non-invertible two-parent rules."""
    num_parents = 2
    is_invertible = False

    def __init__(self, sequent: Sequent) -> None:
        self.sequent = sequent
        prop, side, index = sequent.first_complex_prop()
        self.removed_main_prop = sequent.remove(side, index)
        self.rule = get_rule(prop, side)

    def decompose(self) -> list[tuple[Sequent, Sequent]]:
        rule_result = self.rule.apply()

        decomp_results = []
        for left, right in self.removed_main_prop.possible_mix_parents():
            l_result = Sequent.mix(left, rule_result[0])
            r_result = Sequent.mix(right, rule_result[1])
            decomp_results.append((l_result, r_result))
        return decomp_results

    def get_parents(self) -> list:
        decomp_results = self.decompose()
        parents = []
        for left, right in decomp_results:
            sub_dict = {
                left: None,
                right: None
            }
            parents.append(sub_dict)
        return parents


class Rule(Protocol):
    def apply(self) -> Sequent | tuple[Sequent]:
        ...


class Axiom:
    """Rule for terminating tree branches."""
    def __init__(self, proposition: Proposition = None) -> None:
        self.proposition = proposition

    def apply(self) -> None:
        return None


class LNeg:
    is_invertible = True
    num_parents = 1

    def __init__(self, proposition: Proposition = None) -> None:
        self.proposition = proposition

    def apply(self) -> Sequent:
        """Apply left negation rule to self.sequent."""
        return Sequent((), self.proposition.content)


class RNeg:
    is_invertible = True
    num_parents = 1

    def __init__(self, proposition: Proposition = None) -> None:
        self.proposition = proposition

    def apply(self) -> Sequent:
        """Apply right negation rule to self.sequent."""
        return Sequent(self.proposition.content, ())


class MultLAnd:
    is_invertible = True
    num_parents = 1

    def __init__(self, proposition: Proposition = None) -> None:
        self.proposition = proposition

    def apply(self) -> Sequent:
        """Apply multiplicative left conjunction rule to self.sequent."""
        return Sequent(self.proposition.content, ())


class AddLAnd:
    is_invertible = False
    num_parents = 1

    def __init__(self, proposition: Proposition = None) -> None:
        self.proposition = proposition

    def apply(self) -> tuple[Sequent, Sequent]:
        """Apply additive left conjunction rule to self.sequent."""
        return (Sequent((self.proposition.left,), ()),
                Sequent((self.proposition.right,), ()))


class MultRAnd:
    is_invertible = False
    num_parents = 2

    def __init__(self, proposition: Proposition = None) -> None:
        self.proposition = proposition

    def apply(self) -> tuple[Sequent, Sequent]:
        """Apply multiplicative right conjunction rule to self.sequent."""
        return (
            Sequent((), (self.proposition.left,)),
            Sequent((), (self.proposition.right,))
        )


class AddRAnd:
    is_invertible = True
    num_parents = 2

    def __init__(self, proposition: Proposition = None) -> None:
        self.proposition = proposition

    def apply(self) -> tuple[Sequent, Sequent]:
        """Apply additive right conjunction rule to self.sequent."""
        return (
            Sequent((), (self.proposition.left,)),
            Sequent((), (self.proposition.right,))
        )


class MultLOr:
    is_invertible = False
    num_parents = 2

    def __init__(self, proposition: Proposition = None) -> None:
        self.proposition = proposition

    def apply(self) -> tuple[Sequent, Sequent]:
        """Apply multiplicative left disjunction rule to self.sequent."""
        return (
            Sequent((self.proposition.left,), ()),
            Sequent((self.proposition.right,), ())
        )


class AddLOr:
    is_invertible = True
    num_parents = 2

    def __init__(self, proposition: Proposition = None) -> None:
        self.proposition = proposition

    def apply(self) -> tuple[Sequent, Sequent]:
        """Apply additive left disjunction rule to self.sequent."""
        return (
            Sequent((self.proposition.left,), ()),
            Sequent((self.proposition.right,), ())
        )


class MultROr:
    is_invertible = True
    num_parents = 1

    def __init__(self, proposition: Proposition = None) -> None:
        self.proposition = proposition

    def apply(self) -> Sequent:
        """Apply multiplicative right disjunction rule to self.sequent."""
        return Sequent((), self.proposition.content)


class AddROr:
    is_invertible = False
    num_parents = 1

    def __init__(self, proposition: Proposition = None) -> None:
        self.proposition = proposition

    def apply(self) -> tuple[Sequent, Sequent]:
        """Apply additive right disjunction rule to self.sequent."""
        return (
            Sequent((), (self.proposition.left,)),
            Sequent((), (self.proposition.right,))
        )


class MultLIf:
    is_invertible = False
    num_parents = 2

    def __init__(self, proposition: Proposition = None) -> None:
        self.proposition = proposition

    def apply(self) -> tuple[Sequent, Sequent]:
        """Apply multiplicative left conditional rule to self.sequent."""
        return (
            Sequent((), (self.proposition.left,)),
            Sequent((self.proposition.right,), ())
        )


class AddLIf:
    is_invertible = True
    num_parents = 2

    def __init__(self, proposition: Proposition = None) -> None:
        self.proposition = proposition

    def apply(self) -> tuple[Sequent, Sequent]:
        """Apply additive left conditional rule to self.sequent."""
        return (
            Sequent((), (self.proposition.left,)),
            Sequent((self.proposition.right,), ())
        )


class MultRIf:
    is_invertible = True
    num_parents = 1

    def __init__(self, proposition: Proposition = None) -> None:
        self.proposition = proposition

    def apply(self) -> Sequent:
        """Apply multiplicative right conditional rule to self.sequent."""
        return Sequent((self.proposition.left,), (self.proposition.right,))


class AddRIf:
    is_invertible = False
    num_parents = 1

    def __init__(self, proposition: Proposition = None) -> None:
        self.proposition = proposition

    def apply(self) -> tuple[Sequent, Sequent]:
        """Apply additive right conditional rule to self.sequent."""
        return (
            Sequent((self.proposition.left,), ()),
            Sequent((), (self.proposition.right,))
        )


# Dictionary mapping connectives, sides, and types to their rule class.
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

# Dictionary mapping connectives, sides, and types to their decomposer.
decomposers = {
    '~': {'ant': {
        'add': InvertibleOneParentDecomposer,
        'mul': InvertibleOneParentDecomposer
    }, 'con': {
        'add': InvertibleOneParentDecomposer,
        'mul': InvertibleOneParentDecomposer
    }, },
    '&': {'ant': {
        'add': NonInvertibleOneParentDecomposer,
        'mul': InvertibleOneParentDecomposer
    }, 'con': {
        'add': InvertibleTwoParentDecomposer,
        'mul': NonInvertibleTwoParentDecomposer
    }, },
    'v': {'ant': {
        'add': InvertibleTwoParentDecomposer,
        'mul': NonInvertibleTwoParentDecomposer
    }, 'con': {
        'add': NonInvertibleOneParentDecomposer,
        'mul': InvertibleOneParentDecomposer
    }, },
    '->': {'ant': {
        'add': InvertibleTwoParentDecomposer,
        'mul': NonInvertibleTwoParentDecomposer
    }, 'con': {
        'add': NonInvertibleOneParentDecomposer,
        'mul': InvertibleOneParentDecomposer
    }, }
}


def get_rule_setting(connective, side) -> str:
    """Return 'add' or 'mul' from config.json for this rule."""
    return Settings().get_rule(connective, side)


def get_rule(proposition: Proposition, side: str) -> Rule:
    """
    Return the appropriate Rule class for input proposition and side.
    """
    connective = proposition.symb  # Convenience variable
    if not connective:  # Atoms have no connective
        return Axiom(proposition)
    decomp_type = get_rule_setting(connective, side)  # Query Settings for rule type
    rule = rules[connective][side][decomp_type]  # Query the rules dictionary
    return rule(proposition)


def get_decomposer(sequent: Sequent) -> Decomposer:
    """Return the appropriate decomposer for a given sequent."""
    if sequent.is_atomic:
        return AtomDecomposer(sequent)
    prop, side, index = sequent.first_complex_prop() 
    connective = prop.symb
    decomp_type = get_rule_setting(connective, side) 
    decomposer = decomposers[connective][side][decomp_type]
    return decomposer(sequent)

