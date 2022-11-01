import dominate

from dominate import tags


class HTML:
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
