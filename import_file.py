import json 
import pickle

from pathlib import Path
from typing import Any

from abc import ABC, abstractmethod


class Importer(ABC):
    """
    Abstract Class for file imports.
    """ 
    path: str

    def __init__(self, path) -> None:
        self.path = path

    @abstractmethod
    def import_(self) -> list[str]:
        """Import input file as lines for prover use."""


class TextImporter(Importer):
    """
    Class for importing text files.
    """
    def import_(self) -> list[str]:
        with open(self.path, 'r') as file:
            lines = [line.strip('\n') for line in file.readlines()]
        return lines


class JSONImporter(Importer):
    """
    Class for importing json files.
    """
    def import_(self) -> dict[str, None]:
        with open(self.path, 'r') as file:
            data = json.load(file)
        return data

class ByteImporter(Importer):
    """
    Class for importing bytes-like objects.
    """
    def import_(self) -> Any:
        with open(self.path, 'rb') as file:
            data = pickle.load(file)
        return data


def get_importer(path: str) -> Importer:
    """
    Return the correct Importer type for given input.
    """

    importers = {
        '.txt': TextImporter,
        '.json': JSONImporter
    }
    path_suffix = Path(path).suffix
    if path_suffix not in importers.keys():
        raise KeyError(f'{path_suffix} is not a supported import file type')
    return importers[path_suffix](path)
