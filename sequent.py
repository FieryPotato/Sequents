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
importing this module and creating them from scratch.
"""

__all__ = ['Sequent']

import itertools 

from dataclasses import dataclass
from typing import Protocol


class Proposition(Protocol):
    complexity: int


@dataclass(frozen=True, slots=True, order=True)
class Sequent:
    ant: tuple
    con: tuple
    
    def __post_init__(self):
        for side in self:
            if not isinstance(side, tuple):
                raise ValueError(f'Sequent sides must be of type tuple, not {type(side)}.')

    def __iter__(self):
        yield from (self.ant, self.con)

    def __str__(self) -> str:
        ant_str = ', '.join([str(prop) for prop in self.ant])
        con_str = ', '.join([str(prop) for prop in self.con])
        return f'{ant_str}; {con_str}'

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
        names = {name for side in self for prop in side for name in prop.names}
        return names

    @property
    def complexity(self) -> int:
        """
        Return the total complexity of the sequent, i.e. the sum of
        each proposition's complexity.
        """
        ant_complexity = sum(prop.complexity for prop in self.ant)
        con_complexity = sum(prop.complexity for prop in self.con)
        return ant_complexity + con_complexity

    def remove(self, side: str, index: int) -> 'Sequent':
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
        return Sequent(ant, con)

    @staticmethod
    def mix(*args) -> 'Sequent':
        """
        Return a sequent whose antecedent is the combined antecedents
        of all seqeunts in args, and likewise for consequents.
        """
        new_ant = ()
        new_con = ()
        for arg in args:
            new_ant = new_ant + arg.ant
            new_con = new_con + arg.con
        return Sequent(new_ant, new_con)

    def first_complex_prop(self) ->\
            tuple[Proposition, str, int] | tuple[None, None, None]:
        """
        Return the leftmost complex proposition in the sequent, the
        side of the sequent it's on, and its index on that side. If
        self.is_atomic, return None, None, None.
        """
        for side in ('ant', 'con'):
            for i, prop in enumerate(getattr(self, side)):
                if prop.complexity >= 1:
                    return prop, side, i
        return None, None, None

    def main_connective_arity(self) -> int:
        prop, _, _ = self.first_complex_prop()
        return prop.arity if prop is not None else 0
        

    def possible_mix_parents(self) -> list[tuple['Sequent']]:
        """
        Return a list of all possible parents this sequent may have had
        from an application of mix or another non-invertible rule.
        """
        def two_parent_combinations(props):
            """Yield possible combinations for props into two groups."""
            # Represent which parent had the proposition by allocating True
            # to one and false to the other (in all combinations).
            combinations = itertools.product([True, False], repeat=len(props))
            for combination in combinations:
                # Where x is the left parent and y is the right parent
                x = [props[i] for i, v in enumerate(combination) if v]
                y = [props[i] for i, v in enumerate(combination) if not v]
                yield tuple(x), tuple(y)

        results = []
        for antecedents in two_parent_combinations(self.ant):
            for consequents in two_parent_combinations(self.con):
                left_parent = Sequent(antecedents[0], consequents[0])
                right_parent = Sequent(antecedents[1], consequents[1])
                results.append((left_parent, right_parent))
        return results

