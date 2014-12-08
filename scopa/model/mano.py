#!/usr/bin/env python3

from . import carta


class Mano(list):
    def __init__(self, *carte):
        self.extend(carte)
