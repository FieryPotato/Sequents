import pickle

from tree import Tree


class TreeExporter:
    def __init__(self, tree: Tree) -> None:
        self.tree = tree

    def pickled(self) -> bytes:
        return pickle.dumps(self.tree)

class PickleExporter:
    def __init__(self, data, file) -> None:
        self.data = data
        self.file = file

    def export(self) -> None:
        with open(self.file, 'wb') as f:
            pickle.dump(self.data, f)

