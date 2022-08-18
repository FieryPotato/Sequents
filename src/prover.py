import multiprocessing

from src.convert import string_to_sequent
from src.sequent import Sequent


class Prover:
    """
    Class for converting a list of strings representing sequents into
    sequent objects and then turning those objects into trees.
    """

    def __init__(self, data: list[str]) -> None:
        self.roots: list[Sequent] = [string_to_sequent(s) for s in data]

    def run(self) -> None:
        """
        Turn each sequent in self.roots into a full tree and add it to 
        the forest.
        """
        pass

