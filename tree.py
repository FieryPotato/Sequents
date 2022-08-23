from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Any

from sequent import Sequent
from rules import get_decomposer


@dataclass(slots=True)
class Tree:
    """
    Class representing proof-trees with a Sequent object as the root.
    Applications of sequent rules to each leaf on the tree yield more
    leaves until each leaf at the extremes is atomic.
    """
    root: Sequent
    branches: dict = field(default_factory=dict)
    _is_grown: bool = False

    def __post_init__(self) -> None:
        self.branches.update({self.root: {}})

    @property
    def is_grown(self) -> bool:
        """Return whether tree has been fully proved."""
        return self._is_grown

    def grow(self):
        """
        Solve the root, then recursively solve each branch.
        """
        if self.is_grown:
            raise self.TreeIsGrownError(self)
        decomposer = get_decomposer(self.root)
        parents = decomposer.get_parents()
        self.branches[self.root] = parents
        if parents is not None:
            results = {}
            for parent in self.branches[self.root]:
                if (result := self.grow_branch(parent)) is None:
                    continue
                results.update(result)
            self.branches.update(results)
        self._is_grown = True

    def grow_branch(self, sequent) -> dict | None:
        results = {}
        decomposer = get_decomposer(sequent)
        if (parents := decomposer.get_parents()) is None:
            return None
        else:
            for sequent in parents:
                sub_parents = self.grow_branch(sequent)
                results.update(sub_parents)
        return results

    class TreeIsGrownError(Exception):
        def __init__(self, tree) -> None:
            m = f'The tree beginning in {tree.root} has already been decomposed.'
            super().__init__(m)



def deepest_nodes_are_none(d: dict) -> bool:
    """
    Return True if all branches in d terminate with None.
    Return False if any node terminates in an empty dict.
    """
    if d == {}:
        return False
    for v in d.values():
        if v is None:
            continue
        return deepest_nodes_are_none(v)
    return True
