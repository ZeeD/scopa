#!/usr/bin/env python3

import random
import collections

from . import carta


class Mazzo(list):
    def __init__(self):
        for seme in carta.Seme:
            for valore in carta.Valore:
                self.append(carta.Carta(seme=seme, valore=valore))

    def mischia(self):
        random.shuffle(self)

    def carte(self, n=3):
        return [self.pop() for _ in range(n)]


class Mazzetto(list):
    def punti(self, *mazzetti):
        allunga = len(self) >= max(map(len, mazzetti))
        denara = self._denare() >= max(m._denare() for m in mazzetti)
        settanta = self._settanta() >= max(m._settanta() for m in mazzetti)
        settebello = self._settebello()
        scope = self._scope()

        if allunga:
            print("-->allunga!")
        if denara:
            print("-->denara!")
        if settanta:
            print("-->settanta!")
        if settebello:
            print("-->settebello!")
        for _ in range(scope):
            print("-->scopa!")

        return allunga + denara + settanta + settebello + scope

    def _denare(self):
        return len([c for c in self if c.seme == carta.Seme.denari])

    def _settanta(self):
        '''
                        7   6   Asso    5   4   3   2   Re  Cavallo Fante
        Valore Primiera 21  18  16      15  14  13  12  10  10      10
        '''
        per_seme = collections.defaultdict(list)
        for c in self:
            per_seme[c.seme].append(c)

        # se non ho almeno una carta per ogni seme la settanta non vale
        if len(per_seme) < len(carta.Seme):
            return 0

        def punti(c):
            return {
                carta.Valore.asso: 16,
                carta.Valore.due: 12,
                carta.Valore.tre: 13,
                carta.Valore.quattro: 14,
                carta.Valore.cinque: 15,
                carta.Valore.sei: 18,
                carta.Valore.sette: 21,
                carta.Valore.donna: 10,
                carta.Valore.cavallo: 10,
                carta.Valore.re: 10
            }[c.valore]

        return sum(max(map(punti, cs)) for cs in per_seme.values())

    def _settebello(self):
        for c in self:
            if c.seme == carta.Seme.denari and c.valore == carta.Valore.sette:
                return True
        return False

    def _scope(self):
        return len([c for c in self if c.retro])
