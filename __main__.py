import argparse
import os

from pathlib import Path


#cmd         solve infile [outfile]
#            -   decompose sequents in infile and export the results to

#            outfile (if given) or infile_results.json  
#            
#            print file
#            -   prints trees from file
cmd_help = \
    "solve infile [outfile]\n"\
    "-   decompose sequents in infile and export the results to\n"\
    "outfile (if given) or infile_results.json\n"\
    " \n"\
    "print file\n"\
    "-   prints trees from file"


#help_text = f"""usage: Sequents.py [-h] [cmd ...]
#
#positional arguments: 
#{cmd_help}
#
#options:
#-h,  --h    show this help message and exit
#"""


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
