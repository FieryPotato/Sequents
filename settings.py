import json 
import os 

from pathlib import Path

from typing import Any

parent_dir = Path.cwd()

class _Settings(dict):
    file = os.path.join(parent_dir, 'Sequents/config.json')

    def __init__(self) -> None:
        super().__init__()
        with open(self.file, 'r') as cfg: 
            self.update(json.load(cfg))

    def rules(self, connective: str, side: str) -> str:
        return self['connective_type'][connective][side]


sentinel = None


def Settings() -> _Settings:
    """Getter for _Settings singleton."""
    global sentinel
    if sentinel is None:
        sentinel = _Settings()
    return sentinel

