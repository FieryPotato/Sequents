from typing import Generator

import dominate

from dominate import tags
from dominate.tags import h3
from dominate.util import raw

from HTML import utils
from tree import Tree


class Builder:
    tree_class = \
        "      .tree {\n"\
        "        display: grid;\n"\
        "        justify-content: center;\n"\
        "        align-items: center;\n"\
        "        margin: 10px;\n"\
        "        padding: 10px;\n"\
        "      }\n"
    cell_class = \
        "      .cell {\n"\
        "        text-align: center;\n"\
        "        border-top: 2px solid black;\n"\
        "        padding: 0px 0px 0px 10px;\n"\
        "        margin: 0px 4px 0px 16px;\n"\
        "      }\n"
    tag_class = \
        "      .tag {\n"\
        "        text-align: center;\n"\
        "      }\n"
    boilerplate = tree_class, cell_class, tag_class

    def __init__(self, title='') -> None:
        self.document = dominate.document(title=title)

    def build(self, trees):
        """Build the html document."""
        # style = [self.reformat_for_style_tag(line) for cls in self.boilerplate for line in cls]
        style = tags.style('\n')

        for cls in self.boilerplate:
            style.add(cls)

        for tree in trees:
            template_areas, objects = utils.gridify(tree)
            grid_dict = utils.grid_to_dict(template_areas, objects)
            root = grid_dict.pop('root')

            # class_name excludes trailing cell tag ('-f' in this case)
            # and leading '.'
            class_name = next(iter(grid_dict))[1:-2]

            # Add grid-template-areas to style.
            style.add(self.grid_template_areas(template_areas, class_name=class_name))

            # Add grid-area classes to style.
            style.add(self.grid_area(grid_dict, class_name=class_name))

            # Add indent for closing style tag.
            style.add(' ' * 4)

            # Add tree header to body.
            self.document.body.add(self.tree_title(root))

            # Add tree to body.
            self.document.body.add(self.make_body_tree(grid_dict, class_name=class_name))

        self.document.head.add(style)

    def grid_template_areas(self, template_areas: list[list[str]], class_name: str) -> list[str]:
        """
        Coerce grid-template-areas into the following format:
            ._<root's long string> { grid-template-areas:\n
                <lines from template_areas>\n
                <...>\n
                <last line>;\n
            }\n
        Where angle brackets format like pseudo-code f-strings
        and escaped curly braces are literal.
        """
        result = [f'{" " * 6}.{class_name} {"{"} grid-template-areas:\n']
        for line in template_areas:
            bare_line = ' '.join(line)
            formatted_line = f'{" " * 8}"{raw(bare_line)}"\n'
            result.append(formatted_line)
        result[-1] = result[-1][:-1]
        result[-1] += ';\n'
        result.append(" " * 6 + '}\n')
        return [raw(line) for line in result]

    def grid_area(self, grid_dict: dict[str, str], class_name: str) -> list[str]:
        """Coerce grid-dict keys into grid-area classes for css."""
        result = []
        for id in grid_dict:
            if id == 'root':
                continue
            cls, area = id.split('-')
            result.append(f'{" " * 6}{cls}-{area}' + ' { grid-area: ' + f'{area};' + ' }\n')
        return result

    def make_body_tree(self, grid_dict: dict[str, str], class_name: str) -> list[str]:
        """
        Return the contents of grid_dict as a list of strings which
        will be joined with newlines to form the tree object in HTML.
        """
        with tags.div(cls=f'tree {class_name}') as tree:
            for line_id, content in grid_dict.items():
                line_type = 'tag' if line_id.endswith('t') else 'cell'
                content = utils.replace_with_entities(content)
                line_id = line_id.strip('.')
                with tags.div(cls=f'{line_type} {line_id}') as line:
                    line += raw(content)
                tree += line
        return tree

    def tree_title(self, root: str) -> h3:
        """Return root formatted as a header for the tree."""
        return tags.h3(raw(root))

    @staticmethod
    def reformat_for_style_tag(s: str) -> str:
        """Reformat string for use in style"""
        return ' ' * 6 + s + '\n'

    def save(self, path) -> None:
        """Render and save self.document to path."""
        with open(path, 'w') as f:
            f.write(self.document.render())

