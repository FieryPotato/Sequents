class Prover:
    def __init__(self) -> None:
        self.infile: str | None = None
        self.contents: list | None = None
        self.outfile: str | None = None

    def import_(self, path: str, outfile=None) -> None:
        '''
        Import contents of file to self and sets output file.
        '''
        self.infile = path
        with open(path, 'r') as file:
            #self.contents = self.parse_file(file)
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

#    def parse_file(self, file):
#        '''
#        Return the contents of param file converted to sequents or
#        trees.
#        '''
#        match Path(file.name).stem:
#            case '.txt':
#                lines = file.readlines()
#                results = []
#                for line in lines:
#                    results.append(Convert(line).to_sequent())
                    

