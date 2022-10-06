from typing import Protocol


class Tree(Protocol):
    def height(self) -> int:
        ...

    def width(self) -> int:
        ...


def get_array(tree: Tree) -> list[list[str]]:
    """
    Return a 2d array of strings whose dimensions will fit tree.
    """
    rows = 1 + (2 * tree.height())
    columns = 2 * tree.width()
    return [['.' for _ in range(columns)] for _ in range(rows)]
