from multiprocessing import Pool

from convert import string_to_sequent, sequent_to_tree
from sequent import Sequent


class Prover:
    """
    Class for converting a list of strings representing sequents into
    sequent objects and then turning those objects into trees.
    """

    def __init__(self, data: list[str]) -> None:
        self.roots: list[Sequent] = [string_to_sequent(s) for s in data]
        self.forest = []

    def run(self) -> None:
        """
        Turn each sequent in self.roots into a full tree and add it to 
        the forest.
        """
        # Done with multiprocessing to speed up work with many trees.
        with Pool(processes=1) as pool:
            trees = pool.imap_unordered(tree_from_sequent, self.roots)
            for i, tree in enumerate(trees):
                self.forest.append(tree)

