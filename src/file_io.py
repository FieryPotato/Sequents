from pathlib import Path

from abc import ABC, abstractmethod


class Importer(ABC):
    """
    Abstract Class for file imports.
    """ 
    path: str

    @abstractmethod
    def import_lines(self) -> list[str]:
        """Import input file as lines for prover use."""

    @abstractmethod
    def import_dict(self) -> dict:
        """Import input file as dictionary for printer use."""


class TextImporter(Importer):
    """
    Class for importing text files.
    """
    def __init__(self, path) -> None:
        self.path = path

    def import_lines(self) -> list[str]:
        with open(self.path, 'r') as file:
            lines = [line.strip('\n') for line in file.readlines()]
        return lines

    def import_dict(self) -> dict:
        pass


class JSONImporter(Importer):
    """
    Class for importing json files.
    """

    def import_lines(self) -> list[str]:
        pass

    def import_dict(self) -> dict:
        pass


def get_importer(path: str) -> Importer:
    """
    Return the correct factory type for given input.
    """

    factories = {
        '.txt': TextImporter,
        '.json': JSONImporter
    }
    path_suffix = Path(path).suffix
    if path_suffix not in factories.keys():
        raise KeyError(f'{path_suffix} is not a supported import file type')
    return factories[path_suffix](path)
