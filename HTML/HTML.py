from typing import Iterable, Protocol, Generator

import dominate

import HTML.utils as utils

from dominate import tags

from tree import Tree


class HTML:
    tree_class = ".tree {" \
                 "display: grid;" \
                 "justify-content: center;" \
                 "align-items: center;" \
                 "margin: 10px;" \
                 "padding: 10px;" \
                 "}"
    cell_class = ".cell {" \
                 "text-align: center;" \
                 "border-top: 2px solid black;" \
                 "padding: 0px 0px 0px 10px;" \
                 "margin: 0px 4px 0px 16px;" \
                 "}"
    classes = tree_class, cell_class

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

    def create_head(self, tree_css=None) -> None:
        with self.file.head:
            tags.style(self.generate_stylesheet(tree_css))

    def generate_tree_css(self, tree: Tree) -> tuple[str, str, list]:
        css, objects = utils.gridify(tree)
        root = utils.make_css_key(objects[-1][0])
        grid_dict = utils.grid_to_dict(css, objects)
        title = f'/* {tree.root.long_string} */'
        template_area_lines = [
            '_' + root + ' { grid-template-areas: ',
            '}'
        ]
        for row in css:
            join_row = ' '.join(s for s in row)
            f_row = f'  \'{join_row}\''
            template_area_lines.insert(-1, f_row)
            
        grid_areas = []
        for area in grid_dict.keys():
            tag_index = len(root) + 3
            template_area = area + ' { grid-area: ' + f'{area[tag_index:]}' + '; }'
            grid_areas.append(template_area)

        return title, '\n'.join(template_area_lines), grid_areas
            

    def generate_stylesheet(self, tree_css: list[list[str]] = None) -> list[str]:
        if tree_css is None:
            tree_css = [[]]
        # start stylesheet formatting
        stylesheet = ['\n']

        # add boilerplate classes
        stylesheet.extend(
            ' ' * 6 + css_class + '\n' for css_class in self.classes
        )

        # add tree classes
        stylesheet.extend(
            ' ' * 6 + cls + '\n' for tree in tree_css for cls in tree
        )

        # end stylesheet formatting
        stylesheet.append(' ' * 4)
        return stylesheet

