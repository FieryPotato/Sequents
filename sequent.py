import itertools 

from dataclasses import dataclass

from proposition import Proposition


@dataclass(frozen=True, slots=True)
class Sequent:
    ant: tuple
    con: tuple

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

    @property
    def first_complex_prop(self) ->\
            tuple[Proposition, str, int] | tuple[None, None, None]:
        """
        Return the leftmost complex proposition in the sequent, the
        side of the sequent it's on, and its index on that side. If
        self.is_atomic, return None, None, None. Results are stored
        in self.fcp.
        """
        for side in ('ant', 'con'):
            for i, prop in enumerate(getattr(self, side)):
                if prop.complexity >= 1:
                    return prop, side, i
        else:
            return None, None, None
        

    @property
    def possible_mix_parents(self) -> list[tuple['Sequent']]:
        """
        Return a list of all possible parents this sequent may have had
        from an application of mix or another non-invertible rule.
        """
        def two_parent_combinations(props):
            """Yield possible combinations for props into two groups."""
            combinations = itertools.product([True, False], repeat=len(props))
            for combination in combinations:
                x = [props[i] for i, v in enumerate(combination) if v]
                y = [props[i] for i, v in enumerate(combination) if not v]
                yield tuple(x), tuple(y)
            return (), ()

        results = []
        for antecedents in two_parent_combinations(self.ant):
            for consequents in two_parent_combinations(self.con):
                left_parent = Sequent(antecedents[0], consequents[0])
                right_parent = Sequent(antecedents[1], consequents[1])
                results.append((left_parent, right_parent))
        return results

