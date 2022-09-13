"""
Module containing the Prover class. 

The Prover is initialized with a list of strings, which are converted 
and saved into the instance as a list of sequents. The run method can 
then be called to solve each of those sequents and save the results to
the instance's .forest attribute. 
"""

__all__ = ['Prover']

from multiprocessing import Pool
from typing import Protocol

from convert import string_to_sequent, sequent_to_tree


class Sequent(Protocol):
    ...


class Prover:
    """
    Class for converting a list of strings representing sequents into
    sequent objects and then turning those objects into trees.
    """

    def __init__(self, sequents: list[str], names: set = None) -> None:
        if names is None:
            names = {name for sequent in sequents in for name in sequent.names}
        else: 
            self.names = names
        self.roots: list[Sequent] = [string_to_sequent(s) for s in sequents]
        self.forest = []

    def run(self) -> None:
        """
        Turn each sequent in self.roots into a full tree and add it to 
        the forest.
        """
        self.forest = [
sequent_to_tree(root, names=self.names) for root in self.roots]

    def export(self) -> dict:
        return {
            'names': self.names,
            'forest': self.forest
        }


