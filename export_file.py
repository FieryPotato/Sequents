import json
import pickle

from abc import ABC, abstractmethod
from pathlib import Path
from typing import Any

from tree import Tree
from prover import Prover

    
class Exporter(ABC):
    """Abstract class for exporters."""
    def __init__(self, file, data) -> None:
        self.file = file
        self.data = data

    @abstractmethod
    def export(self) -> None:
        """Process self.data and save to self.file."""


class PickleExporter(Exporter):
    """Class for exporting data as a pickled bytestring."""

    def export(self) -> None:
        """Process self.data and save to self.file."""
        with open(self.file, 'wb') as f:
            pickle.dump(self.data, f)


class JSONExporter(Exporter):
    """Class for exporting data to a .json file."""
    def export(self) -> None:
        """Process self.data and save to self.file."""
        with open(self.file, 'w') as f:
            json.dump(self.data, f)


class HTMLExporter(Exporter):
    """Class for exporting data to an .html file for viewing."""
    def export(self) -> None:
        raise NotImplementedError


def get_exporter(dst: str, data: Any) -> Exporter:
    """Return the desired exporter object."""
    exporters = {
        '': PickleExporter,
        '.json': JSONExporter,
        '.html': HTMLExporter
    }
    if (suffix := Path(dst).suffix) in exporters:
        exporter = exporters[suffix]
    else: 
        raise ValueError(f'{suffix} is not an accepted file extension')
    return exporter(dst, data) 

