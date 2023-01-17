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
from typing import Generator

import decompose
import rules
import utils
from sequent import Sequent


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
    branches: list = field(default_factory=list)

    def __post_init__(self) -> None:
        self.names.update({name for name in self.root.names})

    def height(self) -> int:
        """
        Return the proof height of this tree, which is just the
        complexity of its root.
        """
        # if not self.is_grown:
        #     raise RuntimeError('Trees must be grown to measure their height.')
        # return utils.nested_dict_depth(self.branches)
        ...

    def width(self) -> int:
        """
        Return the number of leaves (axioms) in self if there aren't 
        any list branches (i.e. non-invertible rules) in it. Returns 0 
        if any value in any branch is a list.
        """
        # if not self.is_grown:
        #     raise RuntimeError('Trees must be grown to measure their width.')
        # return utils.count_dict_branches(self.branches)
        ...

    def sequents(self) -> Generator[Sequent, None, None]:
        """ Yields from sequents in self. """
        # if not self.is_grown:
        #     raise RuntimeError('Trees must be grown to inspect their sequents.')
        # yield from utils.nodes_in_dict(self.branches)
        ...

    def grow(self):
        """
        Solve the root, then recursively solve each branch.
        """
        # if self.is_grown:
        #     raise self.TreeIsGrownError(self)
        # self.branches[self.root] = self.grow_branch(self.root)
        # self.is_grown = True

        # No operation if tree si already grown.
        if self.branches:
            return

        # Atomic root means no branches, but this must be distinct from
        # a tree that has not been grown. We use [None] to mark this.
        if self.root.is_atomic:
            self.branches.append(None)
            return

        decomposer = decompose.get_function(sequent=self.root, names=self.names)




    def grow_branch(self, sequent) -> dict | list | None:
        """
        Return the body of the tree whose root is sequent.
        """
        # decomposer = get_decomposer(sequent, names=self.names)
        # if (parents := decomposer.get_parents()) is None:
        #     return None
        # elif isinstance(parents, dict):
        #     return self.grow_dict_branch(parents)
        # elif isinstance(parents, list):
        #     return self.grow_list_branch(parents)
        ...

    def grow_list_branch(self, seq_dict_list: list[dict[Sequent, None]]) \
            -> list[dict[Sequent, Sequent | None]]:
        """
        Return branches expanded from sequents in seq_dict_list.
        """
        # return [
        #     self.grow_dict_branch(sequent) for sequent in seq_dict_list
        # ]
        ...

    def grow_dict_branch(self, seq_dict: dict[Sequent, None]) \
            -> dict[Sequent, Sequent | None]:
        """
        Return branches expanded from sequents in seq_dict.
        """
        # return {
        #     sequent: self.grow_branch(sequent) for sequent in seq_dict.keys()
        # }
        ...


def split_tree(tree) -> list[Tree]:
    """
    Return a list of all possible full trees in tree, where a full tree
    consists only of dict[Sequent, dict | None] pairs. All non-
    invertible rules are split into separate trees, which are identical
    to eac.................................................................................................h other up to the rule application, after which they each
    follow one of the possibilities in the list from
    sequent.possible_mix_parents.
    """
    if (root_parent := tree.branches[tree.root]) is None:
        return [tree]
    result = []
    for sub_tree in utils.split_branch(root_parent):
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
