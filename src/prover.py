class Prover:
    def __init__(self) -> None:
        self.infile: str | None = None
        self.contents: list[str] | None = None
        self.outfile: str | None = None

    def import_(self, path: str, outfile=None) -> None:
        '''
        Import contents of file to self and sets output file.
        '''
        self.infile = path
        with open(path, 'r') as file:
            self.contents = file.readlines()
        if outfile is None:
            self.outfile = ''.join(path.split('.')[:-1]) + '_result.json'
        else:
            self.outfile = outfile

    def export_(self) -> None:
        '''
        Export self.contents to the outfile.
        '''
        with open(self.outfile, 'w') as file:
            file.write(str(self.contents))

