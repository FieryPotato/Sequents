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
    is_grown: bool = False

    def __post_init__(self) -> None:
        self.branches.update({self.root: {}})

    def grow(self):
        """
        Solve the root, then recursively solve each branch.
        """
        if self.is_grown:
            raise self.TreeIsGrownError(self)
        decomposer = get_decomposer(self.root)
        parents = decomposer.get_parents()
        self.branches[self.root] = parents
        if parents is None:
            self.is_grown = True
            return

        results = None

        if isinstance(parents, dict):
            results = self.grow_dict_branch(parents)

        elif isinstance(parents, list):
            results = self.grow_list_branch(parents)

        self.branches[self.root] = results
        self.is_grown = True

    def grow_list_branch(self, seq_dict) -> list:
        """
        Return branches expanded from sequents in seq_dict as a list.
        (For non-invertible rules only.)
        """
        results = []
        for universe in seq_dict:
            parent_results = {}
            parent: Sequent
            for parent in universe:
                branch = self.grow_branch(parent)
                result = {parent: branch}
                parent_results.update(result)
            results.append(parent_results)
        return results

    def grow_dict_branch(self, seq_dict) -> dict:
        """
        Return branches expanded from sequents in seq_dict as a dict.
        (For invertible rules only.)
        """
        results = {}
        parent: Sequent
        for parent in seq_dict:
            branch = self.grow_branch(parent)
            if branch is None:
                result = {parent: None}
            else:
                result = {parent: branch}
            results.update(result)
        return results

    def grow_branch(self, sequent) -> dict | None:
        """
        Return a dict whose only key is sequent and whose value is the
        tree representing its proof.
        """
        results = {}
        decomposer = get_decomposer(sequent)
        if (parents := decomposer.get_parents()) is None:
            return None
        else:
            for sub_sequent in parents:
                if (sub_parents := self.grow_branch(sub_sequent)) is None:
                    sub_parents = {sub_sequent: None}
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
