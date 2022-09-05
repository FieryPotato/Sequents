# Sequents (WIP)


## Overview

This is a spiritual (and hopefully functional) successor to my work in 
MaterialInference. The program has been reimagined and redesigned as a
command-line program that straightforwardly takes in a user-specified
file from the command line, processes it, and outputs a new file in a 
user-specified directory. Processing can later be done on the contents 
of that output file either with this package or with another. 

The Sequents API is vastly improved from the MaterialInference one,
with main classes and functions easily accessible via sane import paths
from the Sequents package. 

As of this writing (2022-09-03) the program applies invertible rules
(by default) to sequents in the input file and saves them as byte strings. 
These can be loaded back up using pickle as follows.
```
>>> import pickle
>>> path = 'path\to\bytes\file'
>>> with open(path, 'rb') as file:
        data = pickle.load(file)
```
The pickle package allows for a more streamlined way to share these objects
between people, uses, and projects, as it allows users to move objects 
directly without the need to translate them to json first, although the 
relevant packages still need to be imported.

Saving to and loading from json is also supported. 
 

## Command-Line Useage

Additivity and multiplicativity of rules can be changed with 
```
$ python3 Sequents set_rule (side) (connective) (value)
```

Current rule settings can be viewed with
```
$ python3 Sequents rules
```

Run the solver and generate a bytes file with
```
$ python3 Sequents solve (infile) [outfile]
```
If outfile is not given, the results are saved to the same directory
as infile.

To save the output as a .json file, use the --json option as below:
```
$ python3 Sequents solve --json (infile) [outfile]
```

## Package Useage
One of the main upsides of the redesign is that the new structure allows
the import of classes using a commonsense syntax. 
```
>>> from Sequents.proposition import *
>>> from Sequents.sequent import Sequent
...
```
See the documentation in each package for more detailed information.

