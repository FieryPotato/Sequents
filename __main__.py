import argparse
import os
import sys

from pathlib import Path

from import_file import get_importer
from prover import Prover
from export_file import get_exporter


solve_help = 'decompose sequents in infile and export the results to '\
             'outfile (if given) or infile_results'


def solve(infile, outfile):
    if outfile is None:
        in_path = Path(infile)
        outfile = in_path.stem + '_results'
    elif (of := Path(outfile)).suffix:  # Trim path suffix of outfile
        while of != of.stem:        # if it has one
            of = of.stem
        outfile = of

    # Import file
    importer = get_importer(infile)
    sequents = importer.import_()

    # Solve sequents in file
    prover = Prover(sequents)
    prover.run()

    # Export data
    exporter = get_exporter(outfile, prover.forest)
    exporter.export()
    

def main():
    # Set up parser
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest='subcommand')
    solver = subparsers.add_parser('solve', help=solve_help)
    solver.add_argument('infile')
    solver.add_argument('outfile', default=None, nargs='?')
    printer = subparsers.add_parser('print')
    printer.add_argument('infile')
    printer.add_argument('outfile', default=None, nargs='?')

    # Parse arguments
    args = parser.parse_args()
    infile = args.infile
    outfile = args.outfile

    # run command
    if args.subcommand == 'solve':
        solve(args.infile, args.outfile)
    elif args.subcommand == 'print':
        print('Printing outfile to infile (Not implemented)')
    else:
        print('Something went wrong.')

if __name__ == '__main__':
    main()
