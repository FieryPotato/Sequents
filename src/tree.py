from abc import ABC, abstractmethod

from src.proposition import Proposition
from src.sequent import Sequent
from src.rules import get_rule


class Tree:
    """
    Class representing proof-trees with a Sequent object as the root.
    Applications of sequent rules to each leaf on the tree yield more
    leaves until each leaf at the extremes is atomic.
    """
    def __init__(self, root: Sequent) -> None:
        self.braches = {}

    def compute_branch(self, sequent: Sequent) -> list[Sequent]:
        """
        Return a list containing the result(s) of decomposing the left-
        most proposition in self.
        """
        rule = get_rule(sequent)
        children = rule.apply()
        if rule.is_invertible:
            # Do invertible branch
        else:
            # Do non-invertible branch

