class Prover:
    def __init__(self) -> None:
        self.import_filename: str | None = None
        self.imported_contents: list[str] | None = None
        self.outfile: str | None = None
        

    def _import(self, path: str, outfile=None) -> None:
        self.import_filename = path
        with open(path, "r") as file:
            self.imported_contents = file.readlines()
        if outfile is None:
            self.outfile = "".join(path.split(".")[:-1]) + "_result.json"
        else:
            self.outfile = outfile

