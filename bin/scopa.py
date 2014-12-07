#!/usr/bin/env python3

# common preamble needed to launch the script from the package
from sys import path
from os import pardir
from os.path import dirname, join
path.append(join(dirname(__file__), pardir, 'scopa'))
# end common preamble


import main

if __name__ == '__main__':
    main.main()
