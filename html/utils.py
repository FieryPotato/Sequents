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

TAG_VALS = {
    0: 'l',
    1: 'r',
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

    root, branches = next(iter(tree.branches.items()))

    # place root tags
    css[1][-1] = 'ft'
    css[2][-1] = 'ft'
    objects[1][-1] = root.tag()
    objects[2][-1] = root.tag()

    for i in range(len(css[0]) - 1):
        css[0][i] = 'f'
        css[1][i] = 'f'
        objects[0][i] = str(root)
        objects[1][i] = str(root)

    if branches is not None:
        css, objects = gridify_branch(
            branches, css, objects, tag='f', x_start=0, x_end=len(css[0]), y=2
        )
    css.reverse()
    objects.reverse()
    return css, objects


def gridify_branch(branch: dict, css: list, objects: list, tag: str = 'f',
        x_start=0, x_end=-1, y=2) -> tuple[list, list]:
    """Returned tuple contains css and objects in that order."""
    match len(branch.values()):
        case 1:
            return gridify_one_parent_branch(
                branch, css, objects, tag, x_start, x_end, y
            )
        case 2:
            return gridify_two_parent_branch(
                branch, css, objects, tag, x_start, x_end, y
            )
        case _:
            raise ValueError(f'Malformed branch: {branch}')

def gridify_two_parent_branch(branch, css, objects, tag, x_start, x_end, y):
    for i, items in enumerate(branch.items()):
        sequent, parents = items
        new_tag = tag + TAG_VALS[i]
        j = i + 1
        x_start = 2 * i
        x_end = 2 * j - 1

        # place objects
        css[y][x_start] = new_tag
        css[y + 1][x_start] = new_tag
        objects[y][x_start] = str(sequent)
        objects[y + 1][x_start] = str(sequent)

        # place tags
        css[y + 1][x_end] = new_tag + 't'
        css[y + 2][x_end] = new_tag + 't'
        objects[y + 1][x_end] = sequent.tag()
        objects[y + 2][x_end] = sequent.tag()
    
        if parents is not None:
            css, objects = gridify_branch(
                parents, css, objects, new_tag, x_start=x_start, x_end=x_end, y=y + 2
            )

    return css, objects


def gridify_one_parent_branch(branch, css, objects, tag, x_start, x_end, y):
    sequent = next(iter(branch.keys()))
    new_tag = tag + 'm'
    array_end = x_end if x_end != len(css[0]) else x_end - 1

    # place objects
    for i in range(x_start, array_end):
        css[y][i] = new_tag
        css[y + 1][i] = new_tag
        objects[y][i] = str(sequent)
        objects[y + 1][i] = str(sequent)

    # place tags
    css[y + 1][array_end] = new_tag + 't'
    css[y + 2][array_end] = new_tag + 't'
    objects[y + 1][array_end] = sequent.tag()
    objects[y + 2][array_end] = sequent.tag()

    if (parent := branch[sequent]) is None:
        return css, objects
    return gridify_branch(
        parent, css, objects, tag=new_tag, x_start=x_start, x_end=x_end, y = y + 2
    )
