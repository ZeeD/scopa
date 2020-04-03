from __future__ import annotations

import collections
import random
import typing

from . import carta


class Mazzo(typing.List[carta.Carta]):
    def __init__(self) -> None:
        super().__init__()
        for seme in carta.Seme:
            for valore in carta.Valore:
                self.append(carta.Carta(seme=seme, valore=valore))

    def mischia(self) -> None:
        random.shuffle(self)

    def carte(self, n: int=3) -> typing.List[carta.Carta]:
        return [self.pop() for _ in range(n)]


class Mazzetto(typing.List[carta.Carta]):
    def punti(self, *mazzetti: Mazzetto) -> int:
        allunga: int = len(self) >= max(map(len, mazzetti))
        denara: int = self._denare() >= max(m._denare() for m in mazzetti)
        settanta: int = self._settanta() >= max(m._settanta() for m in mazzetti)
        settebello: int = self._settebello()
        scope: int = self._scope()

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

    def _denare(self) -> int:
        return len([c for c in self if c.seme == carta.Seme.denari])

    def _settanta(self) -> int:
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

        def punti(c: carta.Carta) -> int:
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

    def _settebello(self) -> bool:
        for c in self:
            if c.seme == carta.Seme.denari and c.valore == carta.Valore.sette:
                return True
        return False

    def _scope(self) -> int:
        return len([c for c in self if c.retro])
