import itertools
import re

from typing import Protocol, Any, Generator

from utils import count_dict_branches


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


CSS_KEY_MAP = {
    ' ': '_',
    '(': '1',
    ')': '2',
    '<': '3',
    '>': '4',
    ',': '5',
    ';': '6'
}


ENTITY_MAP = {
    r';': 'semicolon',
    r'\s&\s': 'ampersand',
    r'&': '&and;',
    r'\sand\s': ' &and; ',
    r'-\>': '&rarr;',
    r'\<': ' &lt; ',
    r'\>': ' &gt; ',
    r'\simplies\s': ' &rarr; ',
    r'v': '&or;',
    r'\sor\s': ' &or; ',
    r'~\s': '&not; ',
    r'not\s': '&not; ',
    r'∀': '&forall;',
    r'forall': '&forall;',
    r'∃': '&exists;',
    r'exists': '&exists;',
    'ampersand': '&and;',
    'semicolon': ' &vdash;',
}


def replace_with_entities(string: str) -> str:
    for pattern, replacement in ENTITY_MAP.items():
        string = re.sub(pattern, replacement, string)
    return string


def get_array(tree: Tree, dtype=None) -> list[list[Any]]:
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
    Return a pair of grids which represent the css grid tags as they
    would appear in a css grid-template-areas property and the objects
    that fill those cells. Note that all subroutines from here on
    modify the css and objects variables defined here.
    """
    css: list[list[str]] = get_array(tree, dtype='css')
    objects: list[list[None]] = get_array(tree, dtype=None)
    root, branches = next(iter(tree.branches.items()))

    css[1][-1] = 'ft'
    css[2][-1] = 'ft'
    root_tag = root.tag()
    objects[1][-1] = root_tag
    objects[2][-1] = root_tag

    for i in range(len(css[0]) - 1):
        css[0][i] = 'f'
        css[1][i] = 'f'
        objects[0][i] = root.long_string
        objects[1][i] = root.long_string

    if branches is not None:
        gridify_branch(
            branches, css, objects, tag='f', x_start=0, x_end=len(css[0]), y=2
        )

    # Because of our order of iteration in subroutines, css and
    # objects are reversed from where they should be.
    css.reverse()
    objects.reverse()
    return css, objects


def gridify_branch(branch: dict, css: list, objects: list, tag: str = 'f',
                   x_start=0, x_end=-1, y=2) -> tuple[list, list]:
    """Returned tuple contains css and objects in that order."""
    match len(branch.values()):
        case 1:
            gridify_one_parent_branch(
                branch, css, objects, tag, x_start, x_end, y
            )
        case 2:
            gridify_two_parent_branch(
                branch, css, objects, tag, x_start, x_end, y
            )
        case _:
            raise ValueError(f'Malformed branch: {branch}')


def gridify_two_parent_branch(branch, css, objects, tag, x_start, x_end, y):
    """
    Returns css and objects (in that order) for two-parent branches
    with the objects in branch added to each.
    """
    # The width of each parent tree, ordered left to right.
    parent_lengths = [
        count_dict_branches(parent)    # Count only returns integers for
        if parent is not None else 1   # non-None parents, so for None
        for parent in branch.values()  # parents we substitute 1.
    ]

    # Prevent index errors trying to access the nth index of a length n list.
    grid_width = len(css[0])
    x_end = x_end if x_end != grid_width else grid_width - 1

    for i, items in enumerate(branch.items()):
        sequent, parents = items
        new_tag = f'{tag}l' if not i else f'{tag}r'

        # Left branches use x_start.
        # Right branches use x_start plus the width of the left branch.
        new_x_start = x_start if not i else x_start + (2 * parent_lengths[0])

        # Left branches use x_start plus the width of the left branch minus 1.
        # Right branches use x_end.
        new_x_end = x_end if i else (x_start + 2 * parent_lengths[0]) - 1

        fill_grids(sequent=sequent, css=css, objects=objects,
                   tag=new_tag, x_start=new_x_start, x_end=new_x_end, y=y)

        if parents is not None:
            gridify_branch(
                branch=parents, css=css, objects=objects, tag=new_tag,
                x_start=new_x_start, x_end=new_x_end, y=y+2
            )

    return css, objects


def gridify_one_parent_branch(branch, css, objects, tag, x_start, x_end, y):
    """
    Returns css and objects (in that order) for one-parent branches
    with the objects in branch added to each.
    """
    sequent = next(iter(branch.keys()))
    new_tag = tag + 'm'
    array_end = x_end if x_end != len(css[0]) else x_end - 1

    fill_grids(sequent, css, objects, new_tag, x_start, array_end, y)

    if (parent := branch[sequent]) is not None:
        gridify_branch(
            branch=parent, css=css, objects=objects, tag=new_tag,
            x_start=x_start, x_end=x_end, y=y+2
        )


def fill_grids(sequent, css, objects, tag, x_start, x_end, y):
    """
    Place each css classes, tags, and objects for sequent into their
    respective arrays.
    """
    for j in range(x_start, x_end):
        css[y][j] = tag
        css[y + 1][j] = tag
        objects[y][j] = sequent.long_string
        objects[y + 1][j] = sequent.long_string
    css[y + 1][x_end] = tag + 't'
    css[y + 2][x_end] = tag + 't'
    
    rule = sequent.tag()
    objects[y + 1][x_end] = rule
    objects[y + 2][x_end] = rule


def css_class_name(sequent: str) -> str:
    """
    Replace protected css class characters with their numeric
    substitutes as defined in CSS_KEY_MAP.
    """
    return ''.join(
        CSS_KEY_MAP[c]
        if c in CSS_KEY_MAP
        else c
        for c in sequent.strip(' ')
    )


def grid_to_dict(css: list[str], objects: list[str | None]) -> dict[str, str]:
    """
    Convert a css and objects array pair into a dictionary mapping
    css classes to the object a div of that class should contain in
    its tree div in HTML.
    """
    grid_height: int = len(css)
    grid_width: int = len(css[0])
    css_root: str = css_class_name(objects[-1][0])
    html_root: str = objects[-1][0]
    result = {'root': html_root}
    grid_dict = {
        f'._{css_root}-{css[y][x]}': objects[y][x]
        for x, y in itertools.product(range(grid_width), range(grid_height))
        if css[y][x] != '.'
    }
    result.update(grid_dict)
    return result


def unnest(iterable, iterable_type=str) -> Generator[str, None, None]:
    """
    Unpacks input nested iterable to whatever it contains. Supports
    setting a type to stop on (defaults to str).
    """
    if hasattr(iterable, '__iter__') and not isinstance(iterable, iterable_type):
        for sub_iterable in iterable:
            yield from unnest(sub_iterable)
    else:
        yield iterable

