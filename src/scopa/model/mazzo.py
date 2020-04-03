'the models for a deck of cards'

from __future__ import annotations

import collections
import random
import typing

from . import carta


class Mazzo:
    'a deck of 40 cards'

    def __init__(self) -> None:
        self._carte = [carta.Carta(seme=seme, valore=valore)
                       for seme in carta.Seme
                       for valore in carta.Valore]

    def mischia(self) -> None:
        'shuffle the cards'

        random.shuffle(self._carte)

    def dai_carte(self, quante: int = 3) -> typing.List[carta.Carta]:
        'takes card from here and give to the player'

        return [self._carte.pop() for _ in range(quante)]

    def ancora_carte(self) -> bool:
        'is here any remaining card?'
        return bool(self._carte)


class Mazzetto:
    'the deck captured by each player'

    def __init__(self) -> None:
        self._mazzetto: typing.List[carta.Carta] = []

    def aggiungi(self,
                 comb: typing.Sequence[carta.Carta],
                 carta_: carta.Carta) -> None:
        'the player has taken comb using carta_ from the play'

        self._mazzetto.extend(comb)
        self._mazzetto.append(carta_)

    def conta(self) -> int:
        'how many cards are here?'

        return len(self._mazzetto)

    def punti(self, *mazzetti: Mazzetto) -> int:
        'calculate the points at the end of the play'

        allunga: int = self.conta() >= max(m.conta() for m in mazzetti)
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
        return len([c for c in self._mazzetto if c.seme == carta.Seme.denari])

    def _settanta(self) -> int:
        '''
                        7   6   Asso    5   4   3   2   Re  Cavallo Fante
        Valore Primiera 21  18  16      15  14  13  12  10  10      10
        '''
        per_seme = collections.defaultdict(list)
        for carta_ in self._mazzetto:
            per_seme[carta_.seme].append(carta_)

        # se non ho almeno una carta per ogni seme la settanta non vale
        if len(per_seme) < len(carta.Seme):
            return 0

        def punti(carta_: carta.Carta) -> int:
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
            }[carta_.valore]

        return sum(max(map(punti, cs)) for cs in per_seme.values())

    def _settebello(self) -> bool:
        for carta_ in self._mazzetto:
            if all((carta_.seme == carta.Seme.denari,
                    carta_.valore == carta.Valore.sette)):
                return True
        return False

    def _scope(self) -> int:
        return len([c for c in self._mazzetto if c.retro])
