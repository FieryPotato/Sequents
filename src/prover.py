from src.file_io import get_importer

class Prover:
    """
    Gets sequent-like strings from a file and outputs a file with those
    sequents developed into full trees.
    """
    def __init__(self, path, outfile) -> None:
        self.infile: path
        self.outfile: outfile
        importer = get_importer(path)
        self.contents = importer.get_lines()

    def import_(self, path: str, outfile=None) -> None:
        """
        Import contents of file to self and sets output file.
        """
        self.infile = path
        with open(path, 'r') as file:
            #self.contents = self.parse_file(file)
            self.contents = file.readlines()
        if outfile is None:
            self.outfile = ''.join(path.split('.')[:-1]) + '_result.json'
        else:
            self.outfile = outfile

