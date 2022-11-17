from typing import Generator

import dominate

from dominate import tags
from dominate.util import raw


from HTML import utils
from tree import Tree


class Builder:
    tree_class = (
        ".tree {",
        "  display: grid;",
        "  justify-content: center;",
        "  align-items: center;",
        "  margin: 10px;",
        "  padding: 10px;",
        "}"
    )
    cell_class = (
        ".cell {",
        "  text-align: center;",
        "  border-top: 2px solid black;",
        "  padding: 0px 0px 0px 10px;",
        "  margin: 0px 4px 0px 16px;",
        "}"
    )
    tag_class = (
        ".tag {",
        "  text-align: center;",
        "}"
    )
    boilerplate = tree_class, cell_class, tag_class

    def __init__(self, title='') -> None:
        self.document = dominate.document(title=title)

    def build(self, trees):
        """Build the html document."""
        style = [self.reformat_for_style_tag(line) for cls in self.boilerplate for line in cls]
        body = []

        for tree in trees:
            template_areas, objects = utils.gridify(tree)
            grid_dict = utils.grid_to_dict(template_areas, objects)
            class_name = utils.css_class_name(grid_dict.pop('root'))
            
            # Add grid-template-areas to style.
            style.extend(self.grid_template_areas(template_areas, class_name=class_name))
            
            # Add grid-area classes to style.
            style.extend(self.grid_area(grid_dict, class_name=class_name))

    
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
        result = [f'._{class_name} {"{"} grid-template-areas:']
        for line in template_areas:
            bare_line = ' '.join(line)
            result.append(bare_line)
        result[-1] += ';'
        result.append('}')
        return result

    def grid_area(self, grid_dict: dict[str, str], class_name: str) -> list[str]:
        """Coerce grid-dict keys into grid-area classes for css."""
        result = []
        for id in grid_dict:
            if id =='root':
                continue
            cls, area = id.split('-')
            result.append(f'{cls}-{area}' + ' { grid-area: ' + f'{area};' + ' }')
        return result 

    def make_body_tree(self, grid_dict: dict[str, str], class_name: str) -> list[str]:
        """
        Return the contents of grid_dict as a list of strings which 
        will be joined with newlines to form the tree object in HTML.
        """
        body = [f'<div class="tree {class_name}">']
        template = '  <div class="{line_type} {line_id}">{content}</div>'
        for line_id, content in grid_dict.items():
            line_type = 'tag' if line_id.endswith('t') else 'cell'
            content = utils.replace_with_entities(content)
            body.append(
                template.format(line_type=line_type, line_id=line_id[1:], content=content)
            )
        body.append('</div>')
        return body

    @staticmethod
    def reformat_for_style_tag(s: str) -> str:
        """Reformat string for use in style"""
        return ' ' * 6 + s + '\n'

    def save(self, path) -> None:
        """Render and save self.document to path."""
        with open(path, 'w') as f:
            f.write(self.document.render())

