import numpy as np

from typing import Protocol


class Tree(Protocol):
    branches: dict

    def height(self) -> int:
        ...

    def width(self) -> int:
        ...


def get_array(tree: Tree) -> np.chararray:
    """
    Return a 2d numpy array of strings whose dimensions will fit tree.
    """
    rows = 1 + (2 * tree.height())
    columns = 2 * tree.width()
    result = np.chararray(shape=(rows, columns))
    result.fill(b'')
    return result


def gridify(tree: Tree) -> tuple[list, list]:
    """
    Return a pair of lists of lists which represent grids in which a
    tree's branches are embedded.
    """
    base = get_array(tree)
    css: np.chararray = base.copy()
    objects: np.chararray = base.copy()

