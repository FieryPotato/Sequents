from dataclasses import dataclass, field

from sequent import Sequent
from rules import get_rule, get_decomposer


@dataclass(slots=True)
class Tree:
    """
    Class representing proof-trees with a Sequent object as the root.
    Applications of sequent rules to each leaf on the tree yield more
    leaves until each leaf at the extremes is atomic.
    """
    root: Sequent
    branches: dict = field(default_factory=dict)

    def __post_init__(self) -> None:
        self.branches.update({self.root: {}})

    @property
    def is_full(self) -> bool:
        """Return whether tree has been fully proved."""
        for value in self.branches.values():
            if value is None:
                continue
            elif not deepest_nodes_are_none(value):
                return False
        return True

    def grow(self):
        """
        Solve the root and each branch it creates until all leaves end
        in None.
        """
        while not self.is_full:
            for root, d in self.branches.items():
                if d == {}:
                    decomposer = get_decomposer(root)
                    result = decomposer.decompose()
                    if result is None:
                        self.branches[root] = None
                    else:
                        self.branches[root] = {
                            result: {}
                        }
                else:
                    for sequent, sub_tree in d.items():
                        if sub_tree == {}:
                            decomposer = get_decomposer(sequent)
                            result = decomposer.decompose()
                            if result is None:
                                d[sequent] = None
                            else:
                                d[sequent] = {
                                    result: {}
                                }


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
