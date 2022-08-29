from multiprocessing import Pool

from convert import string_to_sequent
from sequent import Sequent
from tree import Tree


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
        # Done with multiprocessing to speed up work on big trees.
        with Pool() as pool:
             trees = pool.imap_unordered(self.mk_tree, self.roots)
             for tree in trees:
                 self.forest.append(tree)

    def mk_tree(self, sequent) -> Tree:
        """Return Tree object grown from sequent."""
        tree = Tree(sequent)
        tree.grow()
        return tree

