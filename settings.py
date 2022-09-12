import json
import os

from collections.abc import MutableMapping
from pathlib import Path
from typing import Any


# Absolute path to the Sequents package.
sequent_package_dir = Path(__file__).parents[0]
config_path = os.path.join(sequent_package_dir, 'config.json')


class _Settings(MutableMapping):
    """
    Object for storing and maintaining config.json. It's a singleton to
    prevent the possibility of inconsistent Settings objects.
    """

    def __init__(self) -> None:
        super().__init__()
        self.path = config_path
        self._dict = {}
        with open(self.path, 'r', encoding='utf-8') as cfg:
            self.update(json.load(cfg))

    def __setitem__(self, key, val) -> None:
        self._dict[key] = val
        self.save()

    def __getitem__(self, key) -> Any:
        return self._dict[key]

    def __delitem__(self, key) -> None:
        del self._dict[key]

    def __iter__(self):
        yield from self._dict.__iter__()

    def __len__(self) -> int:
        return len(self._dict)

    def update(self, *args, **kwargs) -> None:
        """
        Update self._dict and save the results to disk.
        """
        self._dict.update(*args, **kwargs)
        self.save()

    def get_rule(self, connective: str, side: str) -> str:
        """Returns rule type from config.json."""
        return self['connective_type'][connective][side]

    def set_rule(self, connective: str, side: str, value) -> None:
        """Change connective rule in self."""
        self['connective_type'][connective][side] = value
        self.save()

    def save(self) -> None:
        """Save contents of self to config.json."""
        with open(self.path, 'w') as f:
            json.dump(self._dict, f, indent=4)

    def print_rules(self) -> None:
        """Print connective rules to console."""
        string = 'Rules:\n' 
        for connective in '&', 'v', '->', '~':
            string += (f'{connective}:\n')
            for side in 'ant', 'con':
                string += (f'    {side}: {self.get_rule(connective, side)}\n')
        print(string)


# Singleton sentinel value
sentinel = None


def Settings() -> _Settings:
    """Getter for _Settings singleton."""
    global sentinel
    if sentinel is None:
        sentinel = _Settings()
    return sentinel
