"""
This package contains classes for exporting data to a given file.

The only function you really need is get_exporter, which takes a
desired output path as input and returns an exporter ready to export
to that file by calling it's .export(data) function. Note that in all
cases, data should be an iterable container of Tree objects.

"""
__all__ = ['get_exporter']

import json
import pickle

from pathlib import Path
from typing import Any, Protocol

    
class Exporter(Protocol):
    """Protocol for exporters."""
    def export(self, data) -> None:
        ...


class PickleExporter:
    """Class for exporting data using pickle.""" 
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
        names = data['names']
        forest = [tree.to_dict() for tree in data['forest']]
        result = {
            'names': names,
            'forest': forest
        }
        with open(self.file, 'w') as f:
            json.dump(result, f, indent=4)


class HTMLExporter:
    """
    Class for exporting data to an .html file for viewing.
    The plan is to eventually be able to typeset trees as an html
    file that can be opened in any web browser. This will not be 
    implemented until I get a handle on html and any relevant 
    javascript.
    """
    def __init__(self, file) -> None:
        self.file = file

    def export(self, data) -> None:
        raise NotImplementedError


def get_exporter(dst: str) -> Exporter:
    """Return the exporter object matching dst's suffix."""
    exporters = {
        '': PickleExporter,
        '.json': JSONExporter,
        '.html': HTMLExporter
    }
    if (suffix := Path(dst).suffix) not in exporters:
        raise ValueError(f'{suffix} is not an accepted file extension')
    exporter = exporters[suffix]
    return exporter(dst) 

