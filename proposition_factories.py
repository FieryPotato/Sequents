from typing import Protocol

from convert import Proposition, string_to_proposition
from proposition import Atom, Negation, Universal, Existential, Conjunction, Disjunction, Conditional


class PropositionFactory(Protocol):
    """Protocol for proposition factories."""

    def get_prop(self, *content) -> Proposition:
        ...


class AtomFactory:
    """Factory for Atoms."""

    def get_prop(self, content) -> Atom:
        """Return an Atom instance."""
        return Atom(content)


class NegationFactory:
    """Factory for Negations."""

    def get_prop(self, _, prop) -> Negation:
        """Return a Negation instance."""
        return Negation(string_to_proposition(prop))


class UniversalFactory:
    """Factory for Universals."""

    def get_prop(self, _, var, prop) -> Universal:
        return Universal(var, string_to_proposition(prop))


class ExistentialFactory:
    """Factory for Existentials."""

    def get_prop(self, _, var, prop) -> Existential:
        return Existential(var, string_to_proposition(prop))


class ConjunctionFactory:
    """Factory for Conjunctions."""

    def get_prop(self, left, _, right) -> Conjunction:
        """Return a Conjunction instance."""
        return Conjunction(
            string_to_proposition(left),
            string_to_proposition(right)
        )


class DisjunctionFactory:
    """Factory for Disjunctions."""

    def get_prop(self, left, _, right) -> Disjunction:
        """Return a Disjunction instance."""
        return Disjunction(
            string_to_proposition(left),
            string_to_proposition(right)
        )


class ConditionalFactory:
    """Factory for Conditionals."""

    def get_prop(self, ant, _, con) -> Conditional:
        """Return a Conditional instance."""
        return Conditional(
            string_to_proposition(ant),
            string_to_proposition(con)
        )