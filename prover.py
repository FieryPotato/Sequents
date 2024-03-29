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


import itertools

from multiprocessing import Pool

import convert
from sequent import Sequent


class Prover:
    """
    Class for converting a list of strings representing sequents into
    sequent objects and then turning those objects into trees.
    """
    def __init__(self, roots: list[Sequent], names: set = None) -> None:
        if names is None:
            names = set()
        self.names = names

        self.roots = roots

        names_in_roots = {name for sequent in roots for name in sequent.names}
        self.names.update(names_in_roots)
        if not self.names:
            self.names = {'NONE'}

        self.forest = []

    def run(self) -> None:
        """
        Turn each sequent in self.roots into a full tree and add it to 
        the forest. Uses parallel processing if there are sufficiently
        many trees to prove.
        """
        # 10 seems like an okay number to start, but at some point I
        # want to figure out what a good cutoff is, where the benefits
        # of parallelism start to outweigh the costs of pool creation.
        # Obviously for small trees differences will be negligible, but
        # I want to be able to throw unbounded numbers of sequents into
        # this without it taking a year to decompose them all,
        # especially if any non-invertible rules are in use.
        if len(self.roots) > 10:
            with Pool() as pool:
                results = pool.starmap(convert.sequent_to_tree, ((root, self.names) for root in self.roots))
        else:
            results = itertools.starmap(convert.sequent_to_tree, ((root, self.names) for root in self.roots))
        self.forest.extend(results)

    def export(self) -> dict:
        """
        Return a dictionary of the prover's names, roots, and solved trees.
        """
        return {
            'names': self.names,
            'sequents': self.roots,
            'forest': self.forest
        }

