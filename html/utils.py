from typing import Protocol


class Tree(Protocol):
    branches: dict

    def height(self) -> int:
        ...

    def width(self) -> int:
        ...

ARRAY_VALS = {
    str: '',
    None: None,
    int: 0,
    'css': '.'
}

def get_array(tree: Tree, dtype=None) -> list[list[str]]:
    """
    Return a 2d list of strings whose dimensions will fit tree. dtype
    is either a builtin type (str, None, or int) or 'css', which fills
    the cell with "'.'".
    """
    rows = 1 + (2 * tree.height())
    columns = 2 * tree.width()
    val = ARRAY_VALS[dtype]
    return [[val for _ in range(columns)] for _ in range(rows)]


def gridify(tree: Tree) -> tuple[list, list]:
    """
    Return a pair of lists of lists which represent grids in which a
    tree's branches are embedded. Returns css and objects in that order.
    """

    css = get_array(tree, dtype='css')
    objects = get_array(tree, dtype=None)
    css, objects = gridify_branch(tree.branches, css, objects)       
    css.reverse()
    objects.reverse()
    return css, objects
        
def gridify_branch(branch: dict, css: list, objects: list,
        x: int = 0, y: int = 0, tag: str = 'f') -> tuple[list, list]:
    """Do the gridify work."""
    for sequent, parents in branch.items():
        rightmost_index: int = len(css[0]) - 1
        if x == y == 0:
            # place tags
            css[1][rightmost_index] = 'ft'
            css[2][rightmost_index] = 'ft'
            objects[1][rightmost_index] = sequent.tag()
            objects[2][rightmost_index] = sequent.tag()

            # place objects
            for i in range(rightmost_index):
                css[0][i] = 'f'
                css[1][i] = 'f'
                objects[0][i] = str(sequent)
                objects[1][i] = str(sequent)

        elif len(parents) == 1:
            # do 1-parent gridification
            pass
    return css, objects

