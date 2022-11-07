from typing import Iterable, Protocol, Generator, Tuple, List

import dominate

import HTML.utils as utils

from dominate import tags

from tree import Tree


class HTML:
    tree_class = [
        ".tree {",
        "  display: grid;",
        "  justify-content: center;",
        "  align-items: center;",
        "  margin: 10px;",
        "  padding: 10px;",
        "}"
    ]
    cell_class = [
        ".cell {",
        "  text-align: center;",
        "  border-top: 2px solid black;",
        "  padding: 0px 0px 0px 10px;",
        "  margin: 0px 4px 0px 16px;",
        "}"
    ]
    boilerplate = tree_class, cell_class

    def __init__(self, out_path, title='', trees: list[Tree] | None = None) -> None:
        if trees is None:
            trees = []
        self.trees = trees
        self.path = out_path
        self.file = dominate.document(title=title)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        self.save()

    def save(self) -> None:
        with open(self.path, 'w') as f:
            f.write(self.file.render())

    def create_head(self, style: list | None = None) -> None:
        if style is None:
            style = []
        with self.file.head:
            tags.style(style)

    def generate_tree_css(self, tree: Tree) -> tuple[str, list[str], list[str]]:
        css, objects = utils.gridify(tree)
        root = utils.make_css_key(objects[-1][0])
        grid_dict = utils.grid_to_dict(css, objects)
        title = f'/* {tree.root.long_string} */'
        template_area_lines = [
            '._' + root + ' { grid-template-areas:',
            '}'
        ]
        for row in css:
            join_row = ' '.join(s for s in row)
            f_row = f'  \'{join_row}\''
            template_area_lines.insert(-1, f_row)
        template_area_lines[-2] += ';'
            
        grid_areas = []
        for area in grid_dict.keys():
            tag_index = len(root) + 3
            template_area = area + ' { grid-area: ' + f'{area[tag_index:]}' + '; }'
            grid_areas.append(template_area)

        return title, template_area_lines, grid_areas
            

    def generate_stylesheet(self, *args) -> list[str]:
        def unnest(obj):
            if hasattr(obj, '__iter__') and not isinstance(obj, str):
                for sub_obj in obj:
                    yield from unnest(sub_obj)
            else:
                yield obj

        lines = [obj for obj in unnest(args)]

        # start stylesheet formatting
        stylesheet = ['\n']

        # add args to stylesheet
        stylesheet.extend(
            ' ' * 6 + line + '\n' for line in lines
        )

        # end stylesheet formatting
        stylesheet.append(' ' * 4)
        return stylesheet

