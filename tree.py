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
    leaves until each leaf at the extremes is atomic (represented by
    {atomic_sequent: None}).
    """
    root: Sequent
    is_grown: bool = field(default=False)
    branches: dict = field(default_factory=dict, init=False)

    def __post_init__(self) -> None:
        self.branches.update({self.root: None})

    def grow(self):
        """Solve the root, then recursively solve each branch."""
        if self.is_grown:
            raise self.TreeIsGrownError(self)
        self.branches[self.root] = self.grow_branch(self.root)
        self.is_grown = True

    def grow_list_branch(self, seq_list: list[dict[Sequent, None]]) \
            -> list[dict[Sequent, Sequent | None]]:
        """
        Return branches expanded from sequents in seq_list.
        (For non-invertible rules only.)
        """
        return [
            {
                parent: self.grow_branch(parent)
                for parent in universe
            }
            for universe in seq_list
        ]

    def grow_dict_branch(self, seq_dict: dict[Sequent, None]) \
            -> dict[Sequent, Sequent | None]:
        """
        Return branches expanded from sequents in seq_dict.
        (For invertible rules only.)
        """
        return {
            parent: self.grow_branch(parent) for parent in seq_dict
        }

    def grow_branch(self, sequent) -> dict | list | None:
        """
        Return the body of the tree whose root is sequent.
        """
        decomposer = get_decomposer(sequent)
        parents: dict[Sequent, None] | list[dict[Sequent, None]] | None
        if (parents := decomposer.get_parents()) is None:
            return None
        else:
            if isinstance(parents, dict):
                results = self.grow_dict_branch(parents)
            elif isinstance(parents, list):
                results = self.grow_list_branch(parents)
        return results

    @classmethod
    def from_dict(cls, dictionary: dict, is_grown: bool = True) -> 'Tree':
        first_key = next(iter(dictionary.keys()))
        tree = cls(first_key, is_grown=is_grown)
        tree.branches = dictionary
        return tree

    class TreeIsGrownError(Exception):
        def __init__(self, tree) -> None:
            m = f'The tree beginning in {tree.root} has already been decomposed.'
            super().__init__(m)

