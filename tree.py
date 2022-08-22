from dataclasses import dataclass, field

from sequent import Sequent
from rules import get_rule

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
        def deepest_node_is_none(d: dict) -> bool:
            for v in d.values():
                if v is None:
                    return True
                elif not v:
                    return False
                return deepest_node_is_none(v)

        for value in self.branches.values():
            if value is None:
                continue
            elif not deepest_node_is_none(value):
                return False
        return True

    def grow(self):
        """
        Solve the root and each branch it creates until all leaves end
        in None.
        """
        while not self.is_full:
            raise NotImplementedError

