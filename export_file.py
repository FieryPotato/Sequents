import pickle

from abc import ABC
from typing import Any

from tree import Tree


class TreeExporter:
    """Class for turning trees into a serializable format."""
    def __init__(self, tree: Tree) -> None:
        self.tree = tree

    def pickled(self) -> bytes:
        """Return self.tree as a pickled bytestring."""
        return pickle.dumps(self.tree)


class Exporter(ABC):
    """Abstract class for exporters."""


class PickleExporter(Exporter):
    """Class for exporting data as a pickled bytestring."""
    def __init__(self, file, data) -> None:
        self.file = file
        self.data = data

    def export(self) -> None:
        """Save self.data to self.file if self.data is bytes."""
        with open(self.file, 'wb') as f:
            pickle.dump(self.data, f)


def get_exporter(dst: str, data: Any) -> Exporter:
    return PickleExporter(dst, data)

