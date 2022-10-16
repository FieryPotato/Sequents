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
    0: 'm',
    1: 'l',
    2: 'r'
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
        css, objects = gridify_branch(branches, css, objects)
    css.reverse()
    objects.reverse()
    return css, objects


def gridify_branch(branch: dict, css: list, objects: list, tag: str = 'f') -> tuple[list, list]:
    """Do the gridify work."""
    match len(branch.values()):
        case 1:
            gridify_one_parent_branch(branch, css, objects, tag)
        case 2:
            gridify_two_parent_branch(branch, css, objects, tag)

    return css, objects


def gridify_two_parent_branch(branch, css, objects, tag):
    for i, items in enumerate(branch.items()):
        sequent, parents = items
        j = i + 1

        # place objects
        css[2][2 * i] = tag + TAG_VALS[j]
        css[3][2 * i] = tag + TAG_VALS[j]
        objects[2][2 * i] = str(sequent)
        objects[3][2 * i] = str(sequent)

        # place tags
        css[3][2 * j - 1] = tag + TAG_VALS[j] + 't'
        css[4][2 * j - 1] = tag + TAG_VALS[j] + 't'
        objects[3][2 * j - 1] = sequent.tag()
        objects[4][2 * j - 1] = sequent.tag()


def gridify_one_parent_branch(branch, css, objects, tag):
    sequent = next(iter(branch.keys()))

    # place objects
    css[2][0] = tag + 'm'
    css[3][0] = tag + 'm'
    objects[2][0] = str(sequent)
    objects[3][0] = str(sequent)

    # place tags
    css[3][-1] = tag + 'mt'
    css[4][-1] = tag + 'mt'
    objects[3][-1] = sequent.tag()
    objects[4][-1] = sequent.tag()
