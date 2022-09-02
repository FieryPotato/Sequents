import json 
import pickle

from pathlib import Path
from typing import Any, Protocol


class Importer(Protocol):
    """
    Protocol for importers.
    """ 
    def __init__(self, path) -> None:
        self.path = path

    def import_(self) -> list[str]:
        """Import input file as lines for prover use."""
        ...


class TextImporter:
    """
    Class for importing text files.
    """
    def __init__(self, path) -> None:
        self.path = path

    def import_(self) -> list[str]:
        with open(self.path, 'r') as file:
            lines = [line.strip('\n') for line in file.readlines()]
        return lines


class JSONImporter:
    """
    Class for importing json files.
    """
    def __init__(self, path) -> None:
        self.path = path

    def import_(self) -> dict[str, None]:
        with open(self.path, 'r') as file:
            data = json.load(file)
        return data

class ByteImporter:
    """
    Class for importing bytes-like objects.
    """
    def __init__(self, path) -> None:
        self.path = path

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
        '.json': JSONImporter,
        '': ByteImporter
    }
    
    path_suffix = Path(path).suffix  # the file extension
    if path_suffix not in importers.keys():
        raise KeyError(f'{path_suffix} is not a supported import file type')
    return importers[path_suffix](path)

