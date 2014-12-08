#!/usr/bin/env python3

import random

from . import carta

class Mazzo(list):
    def __init__(self):
        for seme in carta.Seme:
            for valore in carta.Valore:
                self.append(carta.Carta(seme=seme, valore=valore))

    def mischia(self):
        random.shuffle(self)

    def carte(self, n=3):
        return [ self.pop() for _ in range(n) ]

class Mazzetto(list):
    def __init__(self):
        self.scope = 0

    def punti(self, *altre_mani):
        allunga = len(self) >= max(map(len, altre_mani))
        denara = self._denare() >= max(mano._denare() for mano in altre_mani)
        settanta = self._settanta() >= max(mano._settanta() for mano in altre_mani)
        settebello = self._settebello()

        return allunga + denara + settanta + settebello + self.scope

    def _denare(self):
        return len(c for c in self if c.seme == carta.Seme.denari)

    def _settanta(self):
        return 0

    def _settebello(self):
        for c in self:
            if c.seme == Seme.denari and c.valore == Valore.sette:
                return True
        return False
