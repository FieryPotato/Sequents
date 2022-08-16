from typing import Union
from copy import deepcopy
from dataclasses import dataclass

@dataclass(frozen=True, slots=True)
class Sequent:
    ant: tuple
    con: tuple

    
    @property
    def complexity(self) -> int:
        """
        Return the total complexity of the sequent, i.e. the sum of
        each proposition's complexity.
        """
        ant_complexity = sum(prop.complexity for prop in self.ant)
        con_complexity = sum(prop.complexity for prop in self.con)
        return ant_complexity + con_complexity

    def decomposed(self) -> list["Sequent"]:
        """
        Return a list containing the result(s) of decomposing the left-
        most proposition in self.
        """
        if self.complexity < 1:                       
            raise self.SequentIsAtomicError(self)       
        prop, side = self.first_complex_prop()
        getattr(self, side).remove(prop)
        decomposed_proposition: "tupseq" = prop.decomposed(side)
        sequents = []
        for result in decomposed_proposition:
            copy = deepcopy(self)
            sequents.append(copy.mix(result))
        return sequents
    
    def mix(self, other: Union["Sequent", "tupseq"]) -> "Sequent":
        """
        Return a combination of self and other. Other can be a sequent
        or tupseq (or any object with .ant and .con properties).
        """
        new_ant = self.ant + other.ant
        new_con = self.con + other.con
        return Sequent(new_ant, new_con)
        
    def first_complex_prop(self) -> "Proposition":
        """
        Return the leftmost complex proposition in the sequent.
        """
        for side in ("ant", "con"):
            for prop in getattr(self, side):
                if prop.complexity >= 1:
                    return prop, side

    class SequentIsAtomicError(Exception):
        def __init__(self, sequent):
            string = f"Sequent {sequent} is already atomic."
            super().__init__(string)
       
