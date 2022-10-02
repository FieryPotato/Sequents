"""
Module containing the Tree class.

Trees represent proof trees in this package. Each tree starts with
a root (a sequent) and grows outward by applying rules first to that 
root and then successively to each result until each node is atomic 
(all leaves terminate in None). Each leaf node is represented by a 
dictionary whose keys are sequents and whose values are their parent
sequents. (To analogize, we can imagine the parent of an atom is None,
which we might consider an Axiom or as part of the material base.)

Trees are grown using the .grow() method and will throw an error if 
they are told to grow more than once.

Invertible rules are always represented as dictionaries, either with 
one or with two key-value pairs. Non-invertible rules are instead
represented as lists of dictionaries, where each dictionary is one 
possible way the parents might be (we are, after all, performing root-
first proof searches, so we don't necessarily know how a sequent came
about).

Trees initialization signature is:
Tree(root: str, is_grown: bool = False, names: list[str] = [])
"""

__all__ = ['Tree']

from dataclasses import dataclass, field
from typing import Protocol

import utils
from rules import get_decomposer
from utils import count_dict_nones, split_branch


class Sequent(Protocol):
    names: set
    complexity: int


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
    names: set[str] = field(default_factory=set)
    branches: dict = field(default_factory=dict)

    def __post_init__(self) -> None:
        if not self.branches:
            self.branches.update({self.root: None})
        self.names.update({name for name in self.root.names})

    @property
    def height(self) -> int:
        """
        Return the proof height of this tree, which is just the
        complexity of its root.
        """
        return 1 + self.root.complexity

    def width(self) -> int:
        """
        Return the width of this tree.
        """
        return utils.count_dict_branches(self.branches)



    def leaves(self) -> int:
        """
        Return the number of leaves (axioms) in self if there aren't 
        any list branches (i.e. non-invertible rules) in it. Returns 0 
        if any value in any branch is a list.
        """
        return count_dict_nones(self.branches)


    def grow(self):
        """Solve the root, then recursively solve each branch."""
        if self.is_grown:
            raise self.TreeIsGrownError(self)
        self.branches[self.root] = self.grow_branch(self.root)
        self.is_grown = True

    def grow_branch(self, sequent) -> dict | list | None:
        """
        Return the body of the tree whose root is sequent.
        """
        decomposer = get_decomposer(sequent, names=self.names)
        if (parents := decomposer.get_parents()) is None:
            return None
        elif isinstance(parents, dict):
            return self.grow_dict_branch(parents)
        elif isinstance(parents, list):
            return self.grow_list_branch(parents)

    def grow_list_branch(self, seq_dict_list: list[dict[Sequent, None]]) \
            -> list[dict[Sequent, Sequent | None]]:
        """
        Return branches expanded from sequents in seq_dict_list.
        """
        return [
            self.grow_dict_branch(sequent) for sequent in seq_dict_list
        ]

    def grow_dict_branch(self, seq_dict: dict[Sequent, None]) \
            -> dict[Sequent, Sequent | None]:
        """
        Return branches expanded from sequents in seq_dict.
        """
        return {
            sequent: self.grow_branch(sequent) for sequent in seq_dict.keys()
        }


    class TreeIsGrownError(Exception):
        """Trees should only be able to be grown once."""
        def __init__(self, tree) -> None:
            m = f'The tree beginning in {tree.root} has already been decomposed.'
            super().__init__(m)


def split_tree(tree) -> list[Tree]:
    """
    Return a list of all possible full trees in tree, where a full
    tree consists only of dict[Sequent, dict | None] pairs. All
    non-invertible rules are split into separate trees, which are
    identical until the rule application.
    """
    if (root_parent := tree.branches[tree.root]) is None:
        return [tree]
    result = []
    for sub_tree in split_branch(root_parent):
        new_dict = {tree.root: sub_tree}
        result.append(
            Tree(
                root=tree.root,
                is_grown=True,
                names=tree.names,
                branches=new_dict
            )
        )
    return result


