import json
import pickle

from pathlib import Path
from typing import Any, Protocol

from tree import Tree
from prover import Prover

    
class Exporter(Protocol):
    """Abstract class for exporters."""

    def export(self, data) -> None:
        ...


class PickleExporter:
    """Class for exporting data as a pickled bytestring."""
    def __init__(self, file) -> None:
        self.file = file

    def export(self, data) -> None:
        """Process data and save to self.file."""
        with open(self.file, 'wb') as f:
            pickle.dump(data, f)


class JSONExporter:
    """Class for exporting data to a .json file."""
    def __init__(self, file) -> None:
        self.file = file
    
    def export(self, data) -> None:
        """Process data and save to self.file."""
        with open(self.file, 'w') as f:
            result = [tree.to_dict() for tree in data]
            json.dump(result, f, indent=4)


class HTMLExporter:
    """Class for exporting data to an .html file for viewing."""
    def __init__(self, file) -> None:
        self.file = file

    def export(self, data) -> None:
        raise NotImplementedError


def get_exporter(dst: str) -> Exporter:
    """Return the desired exporter object based on dst suffix."""
    exporters = {
        '': PickleExporter,
        '.json': JSONExporter,
        '.html': HTMLExporter
    }
    if (suffix := Path(dst).suffix) not in exporters:
        raise ValueError(f'{suffix} is not an accepted file extension')
    exporter = exporters[suffix]
    return exporter(dst) 

