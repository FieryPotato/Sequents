import json 
import os 

from pathlib import Path

from typing import Any

# Absolute path to the Sequents package. 
sequent_package_dir = Path(__file__).parents[0]

class _Settings(dict):
    file = os.path.join(sequent_package_dir, 'config.json')

    def __init__(self) -> None:
        super().__init__()
        with open(self.file, 'r') as cfg: 
            self.update(json.load(cfg))

    def update(self, *args) -> None:
        """
        Overwrites dict.update to ensure we save to config.json after 
        changes.
        """
        super().update(*args)
        self.save()

    def get_rule(self, connective: str, side: str) -> str:
        """Returns rule type from config.json."""
        return self['connective_type'][connective][side]

    def set_rule(self, connective: str, side: str, value) -> None:
        """Change connective rule in self."""
        updated = {
            'connective_type': {
                connective: {
                    side: value
                }
            }
        }
        self.update(updated)

    def save(self) -> None:
        """Save contents of self to config.json."""
        with open(self.file, 'w') as f:
            json.dump(self, f, indent=4)

    def print_rules(self) -> None:
        """Print connective rules to console."""
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


# Singleton sentinel value
sentinel = None

def Settings() -> _Settings:
    """Getter for _Settings singleton."""
    global sentinel
    if sentinel is None:
        sentinel = _Settings()
    return sentinel

