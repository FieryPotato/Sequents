from dataclasses import dataclass

from src.proposition import Proposition


@dataclass(frozen=True, slots=True)
class Sequent:
    ant: tuple
    con: tuple

    def __iter__(self):
        return iter(self.ant, self.con)

    @property
    def complexity(self) -> int:
        """
        Return the total complexity of the sequent, i.e. the sum of
        each proposition's complexity.
        """
        ant_complexity = sum(prop.complexity for prop in self.ant)
        con_complexity = sum(prop.complexity for prop in self.con)
        return ant_complexity + con_complexity

#    def decomposed(self) -> list['Sequent']:
#        """
#        Return a list containing the result(s) of decomposing the left-
#        most proposition in self.
#        """
#        if self.complexity < 1:
#            raise self.SequentIsAtomicError(self)
#        prop, side, index = self.first_complex_prop()
#        decomposed_proposition: tuple[tupseq] = prop.decomposed(side)
#        sequents = []
#        for result in decomposed_proposition:
#            ant, con = self.remove(side, index)
#            copy = tupseq(ant, con)
#            sequents.append(Sequent.mix(copy, result))
#        return sequents

    def remove(self, side: str, index: int) -> tuple:
        """
        Return a new sequent object identical to this one but with the
        proposition at side, index removed.
        """
        ant = self.ant
        con = self.con
        if side == 'ant':
            ant = self.ant[:index] + self.ant[1 + index:]
        elif side == 'con':
            con = self.con[:index] + self.con[1 + index:]
        return Sequent(ant, con)

    @staticmethod
    def mix(*args) -> 'Sequent':
        """
        Return a combination of self and other. Other can be a sequent
        or tupseq (or any object with .ant and .con properties).
        """
        new_ant = tuple()
        new_con = tuple()
        for arg in args:
            new_ant = new_ant + arg.ant
            new_con = new_con + arg.con
        return Sequent(new_ant, new_con)

    @property
    def first_complex_prop(self) -> tuple[Proposition, str, int]:
        """
        Return the leftmost complex proposition in the sequent, the
        side of the sequent it's on, and its index on that side.
        """
        for side in ('ant', 'con'):
            for i, prop in enumerate(getattr(self, side)):
                if prop.complexity >= 1:
                    return prop, side, i

    class SequentIsAtomicError(Exception):
        def __init__(self, sequent):
            string = f'Sequent {sequent} is already atomic.'
            super().__init__(string)
