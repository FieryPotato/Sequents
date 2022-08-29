import argparse
import os
import sys

from pathlib import Path

from export_file import get_exporter
from import_file import get_importer
from prover import Prover
from settings import Settings


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
    

def normalize_rule_args(args) -> tuple[str, str, str]:
    """
    Return args namespace values converted to a format that this
    package expects.
    """
    cj = {'and', 'conjunction', '&'}
    dj = {'or', 'disjunction', 'v'}
    cd = {'implies', 'conditional', '->'}
    n = {'not', 'negation', '~'}
    connectives = {
        '&': cj, 
        'v': dj, 
        '->': cd, 
        '~': n
    }

    ant = {'ant', 'antecedent', 'left'}
    con = {'con', 'consequent', 'right'}
    sides = {
        'ant': ant, 
        'con': con
    }
    
    add = {'add', 'additive', '+'}
    mul = {'mul', 'multiplicative', '*', 'x'}
    values = {
        'add': add,
        'mul': mul
    }

    connective: str
    side: str
    value: str
   
    for key, c_set in connectives.items():
        if args.connective in c_set:
            connective = key
            break
   
    for key, s_set in sides.items():
        if args.side in s_set:
            side = key
            break
   
    for key, v_set in values.items():
        if args.value in v_set:
            value = key
            break

    return connective, side, t


def main():
    # Set up parser
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest='subcommand')

    # create solver subparser
    solver = subparsers.add_parser('solve', help=solve_help)
    solver.add_argument('infile', help='file to be imported')
    solver.add_argument('outfile', default=None, 
            nargs='?', help='destination for results file')

    # create subparser for setting rules
    set_rule = subparsers.add_parser('set_rule', help='edit rule settings')
    set_rule.add_argument('side', help='\'ant\' or \'con\'')
    set_rule.add_argument('connective', help='any connective word or symbol')
    set_rule.add_argument('value', help='\'add\' or \'mul\'')

    # create subparser for viewing rules
    view_rules = subparsers.add_parser('view_rules', help='view current rule settings')

    # Parse arguments
    args = parser.parse_args()

    # run command
    if args.subcommand == 'solve':
        solve(args.infile, args.outfile)
    elif args.subcommand == 'set_rule':
        connective, side, value = normalize_rule_args(args)
        Settings().set_rule(connective, side, value)
    elif args.subcommand == 'view_rules':
        Settings().print_rules()
    else:
        print('Unknown command.')

if __name__ == '__main__':
    main()
