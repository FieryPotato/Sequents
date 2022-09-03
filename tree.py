import json 

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from multiprocessing import Pool
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

    def grow_list_branch(self, seq_dict_list: list[dict[Sequent, None]]) \
            -> list[dict[Sequent, Sequent | None]]:
        """
        Return branches expanded from sequents in seq_dict_list.
        (For non-invertible rules only.)
        """
        return [
            self.grow_dict_branch(sequent) for sequent in seq_dict_list
        ]

    def grow_dict_branch(self, seq_dict: dict[Sequent, None]) \
            -> dict[Sequent, Sequent | None]:
        """
        Return branches expanded from sequents in seq_dict.
        (For invertible rules only.)
        """
        return {
            sequent: self.grow_branch(sequent) for sequent in seq_dict.keys()
        }

    def grow_branch(self, sequent) -> dict | list | None:
        """
        Return the body of the tree whose root is sequent.
        """
        decomposer = get_decomposer(sequent)

        if (parents := decomposer.get_parents()) is None:
            return None
        elif isinstance(parents, dict):
            return self.grow_dict_branch(parents)
        elif isinstance(parents, list):
            return self.grow_list_branch(parents)

    def to_dict(self) -> dict:
        """Return self as a dict."""
        def convert(data):
            """Recursively make elements of data json-serializable."""
            result = None
            if isinstance(data, dict):
                result = {str(key): convert(element) 
                          for key, element in data.items()}
            elif isinstance(data, list):
                result = [convert(element) for element in data]
            return result

        return convert(self.branches)

    class TreeIsGrownError(Exception):
        """Trees should only be able to be grown once."""
        def __init__(self, tree) -> None:
            m = f'The tree beginning in {tree.root} has already been decomposed.'
            super().__init__(m)


def tree_from_sequent(sequent) -> Tree:
    """Return Tree object grown from sequent."""
    tree = Tree(sequent)
    tree.grow()
    return tree


def tree_from_dict(dictionary: dict, is_grown: bool = True) -> Tree:
    """Initialize a Tree object from input dictionary."""
    first_key = next(iter(dictionary.keys()))
    tree = Tree(first_key, is_grown=is_grown)
    tree.branches = dictionary
    return tree

