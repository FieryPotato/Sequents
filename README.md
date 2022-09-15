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

As of this writing (2022-09-13) the program applies invertible rules by
default to sequents in the input file and saves them as byte strings. 
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

First-order propositions are now supported. When loading a text file, names
discovered in the sequents and used by the prover. Loading a .json file 
allows the user to specify names (in addition to names discovered in
sequents). I am open to feedback on the precise behaviour of the 
decomposition rules, including adding variants for additive vs 
multiplicative universal and existential decomposition.


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

When loading from a .txt file, the prover expects sequents as a pair
of comma-separated lists of proposions, separated from each other
by a semicolon.

When loading from a .json file, the prover expects three key: value 
pairs:

        - 'names': list containing names for use in the prover
        - 'sequents': list containing sequents to be decomposed
        - 'forest': list containing solved sequents
        
Any missing value is replaced by an empty placeholder.

When loading from a bytes file, the prover expects an iterable 
containing sequents.

## Package Useage
One of the main upsides of the redesign is that the new structure allows
the import of classes using a commonsense syntax. 
```
>>> from Sequents.proposition import *
>>> from Sequents.sequent import Sequent
...
```
See the documentation in each package for more detailed information.

Note that the convert module is much better suited to the creation of
sequent and proposition objects if you're starting with strings, as it
takes all the pain out of creating more and more deeply nested objects.

For example:
```
>>> Sequent(
    (
        Conditional(
            Negation(
                Atom('P<daniel>')
            ),
            Atom('Q<daniel>')
        ),
        Negation(
            Existential(
                'x', 
                Atom('Q<x>')
            )
        )
    ),
    (
        Atom('P<daniel>')
    )
)
```
produces the same result as the much more readable
```
>>> convert.string_to_sequent(
    '(~ P<daniel> -> Q<daniel>), ~ existsx Q<x>; P<daniel>'
)
```
