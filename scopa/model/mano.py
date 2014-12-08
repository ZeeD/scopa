#!/usr/bin/env python3

from . import carta

class Mano(list):   # TODO implementare un OrderedSet
    ''''''
    def __init__(self, *carte):
        self.extend(carte)
