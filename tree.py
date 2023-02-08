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
from typing import Generator, Self

import rules
from sequent import Sequent


@dataclass(frozen=True, slots=True, order=True)
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

    def __radd__(self, other) -> Self:
        return self + other

    def __getitem__(self, item):
        return self.leaves[item]

    def __len__(self) -> int:
        return len(self.leaves)


def _organize_split_parents(split_parents):
    parent_result_length = len(split_parents[0])
    parent_groups = []
    if len(split_parents) == 2:
        for i in range(parent_result_length):
            parent_groups.append(
                (split_parents[0][i], split_parents[1][i])
            )
    elif len(split_parents) == 1:
        for i in range(parent_result_length):
            parent_groups.append(
                (split_parents[0][i],)
            )
    return parent_groups


@dataclass(slots=True, order=True)
class Tree:
    """
    Class representing proof-trees with a Sequent object as the root.
    """
    root: Sequent
    names: set[str] = field(default_factory=set)
    branches: tuple[Branch | None, ...] = ()

    def __post_init__(self) -> None:
        self.names.update(self.root.names)

    @property
    def is_grown(self) -> bool:
        """Return whether this tree's .grow() method has been called."""
        if self.branches:
            return True
        return False

    @property
    def parents(self) -> Generator[Self, None, None]:
        """
        Generates trees from among parents of this sequent.
        """
        for branch in self.branches:
            for leaf in branch:
                yield leaf

    def height(self) -> int:
        """
        Return the proof height of this tree. In other words, the
        greatest number of steps it takes to fully decompose a branch.
        """
        if not self.is_grown:
            self.grow()
        if self.root.is_atomic:
            return 1
        return max(parent.height() for parent in self.parents) + 1

    def width(self) -> int:
        """
        Returns the number of atoms this tree contains.
        """
        if not self.is_grown:
            self.grow()
        if self.root.is_atomic:
            return 1

        return max(sum(parent.width() for parent in branch) for branch in self.branches)

    def sequents(self) -> Generator[Sequent, None, None]:
        """ Yields from sequents in self. """
        if not self.is_grown:
            self.grow()
        if self.root.is_atomic:
            yield self.root
        else:
            yield from (parent.sequents() for branch in self.branches for parent in branch)

    def grow(self):
        """
        Solve the root, then recursively solve each branch.
        """
        # No operation if tree is already grown.
        if self.branches:
            return

        # Atomic root means no branches, but this must be distinguished
        # from a tree that has not been grown. We mark this with (None,)
        if self.root.is_atomic:
            self.branches = (None,)
            return

        rule = rules.get_rule(self.root, names=self.names)
        self.branches = apply_decomposition(rule)

    def split(self) -> list[Self]:
        if not self.is_grown:
            self.grow()

        # Atomic trees have no parents and therefore cannot be split.
        if self.root.is_atomic:
            return [self]

        result = []
        for branch in self.branches:
            split_parents = self._split_branch_parents(branch)

            for group in split_parents:
                new_tree = Tree(
                    root=self.root,
                    names=self.names,
                    branches=(Branch(group),)
                )
                result.append(new_tree)

        return result

    def _split_branch_parents(self, branch) -> list[tuple[Self]]:
        root_first_complex_proposition = self.root.first_complex_prop()
        proposition = root_first_complex_proposition[0]
        arity = proposition.arity

        split_parents = [[] for _ in range(arity)]
        for i, parent in enumerate(branch):
            split_parent: list[Tree] = parent.split()
            split_parents[i].extend(split_parent)

        return _organize_split_parents(split_parents)


def apply_decomposition(rule: rules.Rule) -> tuple[Branch]:
    decomposition_result: rules.decomp_result = rule.apply()
    return branches_from_decomp_result(decomposition_result)


def branches_from_decomp_result(decomposition_result: rules.decomp_result) -> tuple[Branch]:
    branches: tuple = ()
    for decomposition in decomposition_result:
        branches += (branch_from_decomp_result(decomposition),)
    return branches


def branch_from_decomp_result(decomposition: tuple[Sequent, ...]) -> Branch:
    branch = Branch()
    for sequent in decomposition:
        branch += (sub_tree_from_sequent(sequent),)
    return branch


def sub_tree_from_sequent(sequent: Sequent) -> Tree:
    sub_tree = Tree(sequent)
    sub_tree.grow()
    return sub_tree
