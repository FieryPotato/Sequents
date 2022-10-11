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
    tree's branches are embedded.
    """
    css = get_array(tree, dtype='css')
    objects = get_array(tree, dtype=None)
    for sequent, parents in tree.branches.items():
        # place tags
        css[1][len(css[0]) - 1] = 'ft'
        css[2][len(css[0]) - 1] = 'ft'
        objects[1][len(objects[0]) - 1] = sequent.tag()
        objects[2][len(objects[0]) - 1] = sequent.tag()

        # place objects
        for i in range(len(css[0]) - 1):
            css[0][i] = 'f'
            css[1][i] = 'f'
            objects[0][i] = str(sequent)
            objects[1][i] = str(sequent)
    css.reverse()
    objects.reverse()
    return css, objects
        

