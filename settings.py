import json 

class _Settings:
    file = 'config.json'

    def __init__(self) -> None:
        with open(self.file, 'r') as cfg: 
            self.dict = json.load(cfg)


sentinel = None


def Settings() -> _Settings:
    """Getter for _Settings singleton."""
    global sentinel
    if sentinel is None:
        sentinel = _Settings()
    return sentinel

