"""
Module containing the Prover class. 

The Prover is initialized with a list of strings, which are converted 
and saved into the instance as a list of sequents. The run method can 
then be called to solve each of those sequents and save the results to
the instance's .forest attribute. 

If any first-order propositions appear in the solver's input data, but
none of them have names and no names are passed in to the initializer,
then all quantified propositions will be instantiated with the 'NONE'
non-name.
"""

__all__ = ['Prover']


from typing import Protocol

from convert import sequent_to_tree


class Sequent(Protocol):
    ...


class Prover:
    """
    Class for converting a list of strings representing sequents into
    sequent objects and then turning those objects into trees.
    """
    def __init__(self, roots: list[Sequent], names: set = None) -> None:
        if names is None:
            names = set()
        self.names = names

        self.roots: roots

        names_in_roots = {name for sequent in roots for name in sequent.names}
        self.names.update(names_in_roots)
        if not self.names:
            self.names = {'NONE'}

        self.forest = []

    def run(self) -> None:
        """
        Turn each sequent in self.roots into a full tree and add it to 
        the forest.
        """
        for root in self.roots:
            tree = sequent_to_tree(root, names=self.names)
            self.forest.append(tree)

    def export(self) -> dict:
        """
        Return a dictionary of the prover's names, roots, and solved trees.
        """
        return {
            'names': self.names,
            'sequents': self.roots,
            'forest': self.forest
        }

