from typing import Generator

import dominate

from dominate import tags
from dominate.util import raw


from HTML import utils
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
    tag_class = [
        ".tag {",
        "  text-align: center;",
        "}"
    ]
    boilerplate = tree_class, cell_class, tag_class

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
            if area == 'root':
                continue
            tag_index = len(root) + 3
            template_area = area + ' { grid-area: ' + f'{area[tag_index:]}' + '; }'
            grid_areas.append(template_area)

        return title, template_area_lines, grid_areas
            
    def generate_stylesheet(self, *args) -> list[str]:
        lines = [obj for obj in utils.unnest(args)]

        # start stylesheet formatting
        stylesheet = ['\n']

        # add args to stylesheet
        stylesheet.extend(
            ' ' * 6 + line + '\n' for line in lines
        )

        # end stylesheet formatting
        stylesheet.append(' ' * 4)
        return stylesheet

    def generate_body(self, *args) -> list[str]:
        with self.file.body as body:
            for grid in args:
                root = grid.pop('root')
                body.add(tags.h3(raw(root)))
                
                tree_cls = next(iter(grid.keys()))[1:-2]

                with tags.div(cls=f'tree {tree_cls}') as tree:
                    for key, value in grid.items():
                        cls = key[1:]
                        cell_class = 'tag' if key[-1] == 't' else 'cell'
                        div_cls = f'{cell_class} {cls}'
                        text = utils.replace_with_entities(value)
                        tree.add(tags.div(raw(text), cls=div_cls))

