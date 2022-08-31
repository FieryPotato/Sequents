import argparse

from pathlib import Path

from export_file import get_exporter
from import_file import get_importer
from prover import Prover
from settings import Settings


solve_help = 'decompose sequents in infile and export the results to '\
             'outfile (if given) or infile_results'

side_help = '\'ant\', \'antecedent\', \'left\' '\
            'or \'con\', \'consequent\', \'right\''

add_mul_help = '\'add\', \'additive\', \'+\' '\
               'or \'mul\', \'multiplicative\', \'*\', \'x\''

connective_help = '\'->\', \'implies\', \'if\',\'conditional\' '\
                  'or \'v\', \'or\', \'disjunction\' '\
                  'or \'&\', \'and\', \'conjunction\' '\
                  'or \'~\', \'not\', \'negation\''

def solve(infile, outfile, filetype) -> None:
    # Create path for outfile if outfile is not specified
    if outfile is None:
        # Set outfile to infile plus _results
        in_path = Path(infile)
        new_name = f'{in_path.name}_results'
        outfile = str(in_path.with_name(new_name))  # same path, different filename
    else:
        # Remove file extension from outfile
        out_path = Path(outfile)
        outfile = str(out_path.with_suffix(''))  # same path & filename, different suffix

    # Apply desired filetype
    if filetype is not None:
        outfile = apply_filetype(outfile, filetype)

    # Import file
    importer = get_importer(infile)
    sequents = importer.import_()

    # Solve sequents in file
    prover = Prover(sequents)
    prover.run()

    # Export data
    exporter = get_exporter(outfile)
    exporter.export(prover.forest)


def apply_filetype(outfile: str, filetype: str) -> str:
    """Ensure outfile has the desired extension.""" 
    o_f = Path(outfile)
    if o_f.suffix == filetype:
        return outfile
    else:
        return str(o_f.with_suffix(filetype))


def normalize_rule_args(args) -> tuple[str, str, str]:
    """
    Return args namespace values converted to a format that this
    package expects. 
    """
    cj = {'and', 'conjunction', '&'}
    dj = {'or', 'disjunction', 'v'}
    cd = {'implies', 'conditional', '->', 'if'}
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

    def get_item(arg, d) -> str:
        for key, _set in d.items():
            if arg in _set:
                return key
        raise KeyError
   
    try:
        connective = get_item(args.connective, connectives)
        side = get_item(args.side, sides)
        value = get_item(args.value, values)

    except KeyError:
        raise ValueError('Unknown input in .')

    return connective, side, value


def main():
    # Set up parser
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest='subcommand')

    # Create solver subparser
    solver = subparsers.add_parser('solve', help=solve_help)

    # Add file-type optional argument
    file_type = solver.add_mutually_exclusive_group()
    file_type.add_argument('--json', help='save results in a .json file.', action='store_true')
    file_type.add_argument('--html', help='save results in an .html file.', action='store_true')

    # Add solver main arguments.
    solver.add_argument('infile', help='file to be imported')
    solver.add_argument('outfile', default=None, 
            nargs='?', help='destination for results file')

    # Create subparser for setting rules
    set = subparsers.add_parser('set', help='edit rule settings')
    set.add_argument('side', help=side_help)
    set.add_argument('connective', help=connective_help)
    set.add_argument('value', help=add_mul_help)

    # Create subparser for viewing rules
    view_rules = subparsers.add_parser('view_rules', help='view current rule settings')

    # Parse arguments
    args = parser.parse_args()
    
    # Run command
    if args.subcommand == 'solve':
        # Get file type option
        filetype = None
        if args.json:
            filetype = '.json'
        elif args.html:
            raise NotImplementedError('.html is not yet supported')
            # filetype = '.html'
        
        # Run solver
        solve(args.infile, args.outfile, filetype)

    elif args.subcommand == 'set':
        
        # Set rules in config.json 
        connective, side, value = normalize_rule_args(args)
        Settings().set_rule(connective, side, value)

    elif args.subcommand == 'view_rules':
        # Display currently selected rules
        Settings().print_rules()

    else:
        # Argparse prevents this from ever executing, 
        # but I put it here for completeness.
        print('Unknown command.')

if __name__ == '__main__':
    main()
