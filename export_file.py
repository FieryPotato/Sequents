import pickle

from abc import ABC, abstractmethod
from typing import Any

from tree import Tree
from prover import Prover

    
class Exporter(ABC):
    """Abstract class for exporters."""
    def __init__(self, file, data) -> None:
        self.file = file
        self.data = data
        self.converter = self.convert_type(data)

    @abstractmethod
    def export(self) -> None:
        """Process self.data and save to self.file."""


class Converter(ABC):
    """Abstract class for converting data into a savable format."""
    def __init__(self, data: Any) -> None:
        self.data = data

    @abstractmethod
    def convert(self) -> Any:
        """Process and return self.data."""


class Pickler(Converter):
    def convert(self) -> bytes:
        """Return self.data as a pickled bytestring."""
        return pickle.dumps(self.data)


class PickleExporter(Exporter):
    """Class for exporting data as a pickled bytestring."""
    convert_type = Pickler

    def export(self) -> None:
        """Process self.data and save to self.file."""
        outbound = self.converter.convert()
        with open(self.file, 'wb') as f:
            pickle.dump(outbound, f)


def get_exporter(dst: str, data: Any) -> Exporter:
    """Return the desired exporter object."""
    # JSON and HTML exporters not yet implemented.
    return PickleExporter(dst, data) 

