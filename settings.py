import json 
import os 

from pathlib import Path

from typing import Any

parent_dir = Path(__file__).parents[0]

class _Settings(dict):
    file = os.path.join(parent_dir, 'config.json')

    def __init__(self) -> None:
        super().__init__()
        with open(self.file, 'r') as cfg: 
            self.update(json.load(cfg))

    def update(self, *args) -> None:
        super().update(*args)
        self.save()

    def get_rule(self, connective: str, side: str) -> str:
        return self['connective_type'][connective][side]

    def set_rule(self, connective: str, 
            side: str, value) -> None:
        updated = {
            'connective_type': {
                connective: {
                    side: value
                }
            }
        }
        self.update(updated)

    def save(self) -> None:
        with open(self.file, 'w') as f:
            json.dump(self, f, indent=4)

    def print_rules(self) -> None:
        string = 'Rules:\n'\
            f'&:  ant={self.get_rule("&", "ant")}\n'\
            f'    con={self.get_rule("&", "con")}\n'\
            f'v:  ant={self.get_rule("v", "ant")}\n'\
            f'    con={self.get_rule("v", "con")}\n'\
            f'->: ant={self.get_rule("->", "ant")}\n'\
            f'    con={self.get_rule("->", "con")}\n'\
            f'~:  ant={self.get_rule("~", "ant")}\n'\
            f'    con={self.get_rule("~", "con")}\n'
        print(string)

sentinel = None


def Settings() -> _Settings:
    """Getter for _Settings singleton."""
    global sentinel
    if sentinel is None:
        sentinel = _Settings()
    return sentinel

