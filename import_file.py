"""
Package for handling importing the contents of files into the current
namespace. get_importer takes a path to the file to be imported and 
returns an Importer object of the correct type to load its contents
using the .import_() method. Note that currently only .json, .txt, and 
bytes files are supported import file types. 

Text files are imported as a list of strings, JSON files are imported 
as dictionaries and bytes are imported as whatever was pickled in them.
Notably, this means that you should only import data you trust, as 
Python's pickle module allows for abritrary code execution if used 
improperly.
"""

__all__ = ['get_importer']

import json 
import pickle

from pathlib import Path
from typing import Any, Protocol


class Importer(Protocol):
    """
    Protocol for importers.
    """ 
    def import_(self) -> dict:
        """Import input file as lines for prover use."""
        ...


class TextImporter:
    """
    Class for importing text files.
    """
    def __init__(self, path) -> None:
        self.path = path

    def import_(self) -> dict:
        """Return a list of self.path's lines."""
        with open(self.path, 'r') as file:
            lines = [line.strip('\n') for line in file.readlines()]
        return {
            'names': set(),
            'sequents': lines
        }


class JSONImporter:
    """
    Class for importing json files.
    """
    def __init__(self, path) -> None:
        self.path = path

    def import_(self) -> dict:
        """Return a dictionary represented by the JSON in self.path."""
        with open(self.path, 'r') as file:
            data = json.load(file)
        if 'names' not in data:
            data['names'] = set()
        if 'sequents' not in data:
            data['sequents'] = []
        if 'forest' not in data: 
            data['forest'] = []
        return data

class ByteImporter:
    """
    Class for importing bytes-like objects.
    """
    def __init__(self, path) -> dict:
        self.path = path

    def import_(self) -> Any:
        """Return pickled data from self.path."""
        with open(self.path, 'rb') as file:
            data = pickle.load(file)
        return data


def get_importer(src: str) -> Importer:
    """
    Return the Importer object suited to import src's filetype.
    """
    importers = {
        '.txt': TextImporter,
        '.json': JSONImporter,
        '': ByteImporter
    }
    
    suffix = Path(src).suffix  # the file extension
    if suffix not in importers.keys():
        raise KeyError(f'{suffix} is not a supported import file type')
    return importers[suffix](src)

