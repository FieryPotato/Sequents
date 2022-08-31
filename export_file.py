import json
import pickle

from abc import ABC, abstractmethod
from pathlib import Path
from typing import Any

from tree import Tree
from prover import Prover

    
class Exporter(ABC):
    """Abstract class for exporters."""
    def __init__(self, file) -> None:
        self.file = file

    @abstractmethod
    def export(self, data) -> None:
        """Process data and save to self.file."""


class PickleExporter(Exporter):
    """Class for exporting data as a pickled bytestring."""

    def export(self, data) -> None:
        """Process data and save to self.file."""
        with open(self.file, 'wb') as f:
            pickle.dump(data, f)


class JSONExporter(Exporter):
    """Class for exporting data to a .json file."""
    def export(self, data) -> None:
        """Process data and save to self.file."""
        with open(self.file, 'w') as f:
            result = [tree.to_dict() for tree in data]
            json.dump(result, f, indent=4)


class HTMLExporter(Exporter):
    """Class for exporting data to an .html file for viewing."""
    def export(self, data) -> None:
        raise NotImplementedError


def get_exporter(dst: str) -> Exporter:
    """Return the desired exporter object based on dst suffix."""
    exporters = {
        '': PickleExporter,
        '.json': JSONExporter,
        '.html': HTMLExporter
    }
    if (suffix := Path(dst).suffix) in exporters:
        exporter = exporters[suffix]
    else: 
        raise ValueError(f'{suffix} is not an accepted file extension')
    return exporter(dst) 

