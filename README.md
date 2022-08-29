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

As of this writing (2022-08-29) the package applies invertible rules
(by default) to sequents in the input file and saves them as byte strings. 
These can be loaded up with the built-in pickle package as follows:
```
>>> import pickle
>>> path = 'path\to\bytes\file'
>>> with open(path, 'rb') as file:
        results = pickle.load(file)
```
Current plans are to allow saving to json for a more transparent results file
and as a html document, which will allow users to view the trees typeset in a 
browser window.


## Useage

Additivity and multiplicativity of rules can be changed with 
```
$ python3 Sequents set_rule (side) (connective) (value)
```

Current rule settings can be viewed with
```
$ python3 Sequents view_rules
```

Run the solver (and generate a bytes file) with
```
$ python3 Sequents solve (infile) [outfile]
```
If outfile is not given, the results are saved to the same directory
as infile.

