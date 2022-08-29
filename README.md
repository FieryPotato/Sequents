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

As of this writing (2022-08-28) the package applies invertible rules
to sequents in the input file and saves them as byte strings. These can
be loaded up with the built-in pickle package as follows:
```
>>> import pickle
>>> path = 'path\to\bytes\file'
>>> with open(path, 'rb') as file:
        results = pickle.load(file)
```

