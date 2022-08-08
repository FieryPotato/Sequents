import argparse
import os

from pathlib import Path


cmd_help = \
    "solve infile [outfile]\n"\
    "-   decompose sequents in infile and export the results to\n"\
    "outfile (if given) or infile_results.json\n"\
    " \n"\
    "print file\n"\
    "-   prints trees from file"


def main():
    parser = argparse.ArgumentParser(
            formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument("cmd", nargs="*", help=cmd_help, 
            choices=["solve", "print"])
    
    args = parser.parse_args()

    match cmd := args.cmd:
        case ["solve", infile, *outfile]:
            print(f"solving {infile} to {outfile[0] if outfile else (Path(infile).stem + '_result.txt')}")
        case ["print", file]:
            print(f"printing {file}")
        case _:
            print("Unsupported argument.")
            parser.print_help()


if __name__ == "__main__":
    main()
