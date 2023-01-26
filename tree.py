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
from typing import Generator, Self, Tuple

import rules
import utils
from sequent import Sequent


@dataclass(frozen=True, slots=True)
class Branch:
    """
    A fancy tuple, whose goal is to make reasoning about the
    abstraction easier. Each Branch symbolizes a possible way the
    parents of any sequent might be.

    Specifically, each one-parent non-invertible tree will contain a
    number of branches equal to the number of possible parents that
    tree has, each containing one parent sequent (one leaf), and each
    two-parent non-invertible tree will contain a number of branches
    equal to the number of possible pairs of parents the root sequent
    has (i.e. 2^n, where n is the number of additional propositions in
    the sequent).

    Invertible sequents have exactly one branch and atomic sequents
    have none.
    """
    leaves: tuple = ()

    def __add__(self, other) -> Self:
        added = ()
        if isinstance(other, Branch):
            added = other.leaves
        elif isinstance(other, tuple):
            added = other
        return Branch(self.leaves + added)

    def __getitem__(self, item):
        return self.leaves[item]

    def __len__(self) -> int:
        return len(self.leaves)


@dataclass(slots=True, order=True)
class Tree:
    """
    Class representing proof-trees with a Sequent object as the root.
    """
    root: Sequent
    names: set[str] = field(default_factory=set)
    branches: tuple[Branch | None, ...] = ()

    def __post_init__(self) -> None:
        self.names.update({name for name in self.root.names})

    @property
    def is_grown(self) -> bool:
        """Return whether this tree's .grow() method has been called."""
        if not self.branches:
            return False
        if self.branches[0] is not None:
            return False
        return True

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
        # No operation if tree is already grown.
        if self.branches:
            return

        # Atomic root means no branches, but this must be distinct from
        # a tree that has not been grown. We use [None] to mark this.
        if self.root.is_atomic:
            self.branches = None,
            return

        rule = rules.get_rule(self.root, names=self.names)
        if rule.invertible:
            if rule.parents == 1:
                self.branches = decompose_one_parent_invertible(rule)
            elif rule.parents == 2:
                self.branches = decompose_two_parent_invertible(rule)
        else:
            if rule.parents == 1:
                self.branches = decompose_one_parent_non_invertible(rule)
            elif rule.parents == 2:
                self.branches = decompose_two_parent_non_invertible(rule)


def decompose_one_parent_invertible(rule: rules.Rule) -> tuple[Branch]:
    result_sequents: tuple[tuple[Sequent]] = rule.apply()
    results: tuple = ()
    for result in result_sequents:
        branch = Branch()
        for sequent in result:
            sub_tree = Tree(sequent)
            sub_tree.grow()
            branch += (sub_tree,)
        results += (branch,)
    return results


def decompose_two_parent_invertible(rule: rules.Rule) -> tuple[Branch]:
    result_sequents: tuple[tuple[Sequent, Sequent]] = rule.apply()
    results: tuple = ()
    for result in result_sequents:
        branch = Branch()
        for sequent in result:
            sub_tree = Tree(sequent)
            sub_tree.grow()
            branch += (sub_tree,)
        results += (branch,)
    return results


def decompose_one_parent_non_invertible(rule: rules.Rule) -> tuple[Branch]:
    result_sequents: tuple[tuple[Sequent], ...] = rule.apply()
    results: tuple = ()
    for result in result_sequents:
        branch = Branch()
        for sequent in result:
            sub_tree = Tree(sequent)
            sub_tree.grow()
            branch += (sub_tree,)
        results += (branch,)
    return results


def decompose_two_parent_non_invertible(rule: rules.Rule) -> tuple[Branch]:
    result_sequents: tuple[tuple[Sequent, Sequent], ...] = rule.apply()
    results: tuple = ()
    for result in result_sequents:
        branch = Branch()
        for sequent in result:
            sub_tree = Tree(sequent)
            sub_tree.grow()
            branch += (sub_tree,)
        results += (branch,)
    return results


def split_tree(tree) -> list[Tree]:
    """
    Return a list of all possible full trees in tree, where a full tree
    consists only of dict[Sequent, dict | None] pairs. All non-
    invertible rules are split into separate trees, which are identical
    to each other up to the rule application, after which they each
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
