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
        outfile = infile + '_results'
    elif (of := Path(outfile)).suffix:
        while of != of.stem:
            of = of.stem
        outfile = of
    importer = get_importer(infile)
    data = importer.import_()
    prover = Prover(data)
    prover.run()
    exporter = get_exporter(outfile, data)
    exporter.export()
    

def main():
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest='subcommand')
    solver = subparsers.add_parser('solve')
    solver.add_argument('infile')
    solver.add_argument('outfile', default=None, nargs='?')
    printer = subparsers.add_parser('print')
    printer.add_argument('infile')
    printer.add_argument('outfile', default=None, nargs='?')
    
    args = parser.parse_args()
    infile = args.infile
    outfile = args.outfile
    if args.subcommand == 'solve':
        solve(args.infile, args.outfile)
    else:
        print('Something went wrong.')

if __name__ == '__main__':
    main()
