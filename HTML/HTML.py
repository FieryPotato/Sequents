from typing import Iterable, Protocol

import dominate

from dominate import tags


class Tree(Protocol):
    ...


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

    def __init__(self, out_path, title='') -> None:
        self.path = out_path
        self.file = dominate.document(title=title)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        self.save()

    def save(self) -> None:
        with open(self.path, 'w') as f:
            f.write(self.file.render())

    def create_head(self) -> None:
        with self.file.head:
            # start stylesheet formatting
            stylesheet = ['\n']
            # add class stylings
            stylesheet.extend(
                    ' ' * 6 + css_class + '\n' for css_class in self.classes
            )
            # end stylesheet formatting
            stylesheet.append(' ' * 4)
            # typeset stylesheet
            tags.style(stylesheet)

    def typeset(self, trees: Iterable[Tree]):
        pass
