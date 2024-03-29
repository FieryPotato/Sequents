"""
Module containing the Sequent class.

Sequents are immutable hashable objects containing two tuples of
Propositions and which have the following properties:
    - is_atomic: True if all the sequent's propositions are atomic 
    (i.e. are atoms) and False otherwise.
    - complexity: The total complexity of each proposition in thes 
    sequent.
    
Sequents can be mixed, which is to say two or more sequents can be 
combined into a new sequent whose antecedent is all their combined 
antecedents and likewise for consequents.
>>> s_0 = Sequent((Atom('ant_0'),), (Atom('con_0'),))
>>> s_1 = Sequent((Atom('ant_1'),), (Atom('con_1'),))
>>> Sequent.mix(s_0, s_1)
Sequent((Atom('ant_0'), Atom('ant_1')), (Atom('con_0'), Atom('con_1)))

Sequents know the location of their first complex prop. The following 
returns the proposition, which side it's on, and its index in that 
side. Returns a tuple of three Nones if the sequent is atomic.
>>> s = Sequent((Atom('ant'),), (Conditional(Atom('p'), Atom('q')),))
>>> s.first_complex_prop()
Conditional(Atom('p'), Atom('q')), 'con', 0

Finally, sequents can imperfectly reverse the mixing process. 
Sequent.possible_mix_parents() returns a list containing each pair
of sequents that could have been mixed (or combined via two-parent 
non-invertible rule) to achieve it.

Note that for most purposes, you should prefer to create sequents 
using the string_to_sequent function in the convert module, rather than
importing this module and creating them from scratch, not least because
it's very easy to input bare propositions rather than single-item
tuples or to put in a list. If there's need for a function to turn
other data types into sequents, I'll add one there.
"""

__all__ = ['Sequent']

import itertools
from dataclasses import dataclass, field
from typing import Self, Iterable, Generator

from proposition import Proposition


@dataclass(slots=True, order=True)
class Sequent:
    ant: tuple[Proposition, ...] | Proposition | None
    con: tuple[Proposition, ...] | Proposition | None
    _first_complex_prop: tuple[Proposition, str, int] = field(default=None, init=False)

    def __post_init__(self):
        # Ensure self.ant and self.con contain tuples of propositions
        for attr in 'ant', 'con':
            if getattr(self, attr) is None:
                setattr(self, attr, ())
                continue
            if not isinstance(getattr(self, attr), tuple):
                # Create a list to avoid tuple() using the proposition's
                # .__iter__() for tuple construction.
                side = [getattr(self, attr)]
                setattr(self, attr, tuple(side))

    def __iter__(self):
        yield self.ant
        yield self.con

    def __str__(self) -> str:
        ant_str = ', '.join(map(str, self.ant))
        con_str = ', '.join(map(str, self.con))
        return f'{ant_str}; {con_str}'

    def __hash__(self):
        """
        What makes a sequent unique is the contents of its antecedent
        and consequent as well as where the divider is between the two.
        """
        return hash(self.ant + ('|-',) + self.con)

    def __eq__(self, other):
        if not isinstance(other, Sequent):
            return False
        return self.ant == other.ant and self.con == other.con

    @property
    def is_atomic(self) -> bool:
        """Return whether all propositions in self are atomic."""
        for side in self:
            for prop in side:
                if prop.complexity > 0:
                    return False
        return True

    @property
    def names(self) -> set[str]:
        # this set comprehension saves like 5 lines of nested for loops.
        # It just collects all the names from all the props in self into a set.
        return {name for side in self for prop in side for name in prop.names}

    @property
    def complexity(self) -> int:
        """
        Return the total complexity of the sequent, i.e. the sum of
        each proposition's complexity.
        """
        ant_complexity = sum(prop.complexity for prop in self.ant)
        con_complexity = sum(prop.complexity for prop in self.con)
        return ant_complexity + con_complexity

    @property
    def long_string(self) -> str:
        ant_str = ', '.join(prop.long_string for prop in self.ant)
        con_str = ', '.join(prop.long_string for prop in self.con)
        return f'{ant_str}; {con_str}'

    def remove_proposition_at(self, side: str, index: int) -> Self:
        """
        Return a new sequent object identical to this one but with the
        proposition at side, index removed.
        """
        if side == 'ant':
            ant = self.ant[:index] + self.ant[1 + index:]
            con = self.con
        elif side == 'con':
            ant = self.ant
            con = self.con[:index] + self.con[1 + index:]
        else:
            raise ValueError(f'Parameter "side" must be "ant" or "con", not {side}.')
        return Sequent(ant, con)

    def mix(*sequents: tuple[Self] | Self) -> Self:
        """
        Return a sequent whose antecedent is the combined antecedents
        of the input sequents, and likewise for consequents.

        Can be called either as a static method or as an instance method.
        Where s0, s1, and s2 are sequents:
        >>> Sequent.mix(s0, s1, s2) == s0.mix(s1, s2)
        True
        Order matters
        """
        return Sequent(
            ant=sum((sequent.ant for sequent in sequents), ()),
            con=sum((sequent.con for sequent in sequents), ())
        )

    def tag(self) -> str:
        """
        Return a string representing the rule to be applied to the 
        first complex proposition in self.
        """
        if (proposition := self.first_complex_prop()) is None:
            return 'Ax'
        else:
            symbol = proposition[0].symb
            side = proposition[1]
            side_map = {'ant': 'L', 'con': 'R'}
            return side_map[side] + symbol

    def first_complex_prop(self) -> tuple[Proposition, str, int] | None:
        """
        Return the leftmost complex proposition in the sequent, the
        side of the sequent it's on, and its index on that side. If
        self.is_atomic, return None.
        """
        # Check that we haven't already checked this.
        if self._first_complex_prop is not None:
            return self._first_complex_prop

        # All these returns are to get around the fact that we want to
        # have a nested for loop (because we both iterate and return side)
        for side in ('ant', 'con'):
            for i, prop in enumerate(getattr(self, side)):
                if prop.complexity >= 1:
                    self._first_complex_prop = prop, side, i
                    return self._first_complex_prop

        # Explicit `return None` if self.is_atomic.
        # I would call self.is_atomic to check, but actually the implementation
        # here just does the same steps so if it's not atomic we would end up doing
        # a whole loop through each proposition in each side twice.
        return None

    def possible_mix_parents(self) -> list[tuple[Self, Self]]:
        """
        Return a list of all possible parents this sequent may have had
        from an application of mix or another non-invertible rule.
        """
        combinations = itertools.product(
            binary_combinations(self.ant),
            binary_combinations(self.con)
        )
        return [
            (
                Sequent(antecedents[0], consequents[0]),
                Sequent(antecedents[1], consequents[1])
            )
            for antecedents, consequents in combinations
        ]


def binary_combinations(data: tuple) -> Generator[tuple[tuple, tuple], None, None]:
    """
    Yields all possible ways to split input data into two groups.
    """
    # Represent which parent had the proposition by allocating True
    # to one and false to the other (in all combinations).
    combinations = itertools.product([True, False], repeat=len(data))
    for combination in combinations:
        x = [data[i] for i, v in enumerate(combination) if v]
        y = [data[i] for i, v in enumerate(combination) if not v]
        yield tuple(x), tuple(y)