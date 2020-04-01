#!/usr/bin/env python3

import itertools
import random
import typing

from .model import carta
from .model import mano
from .model import mazzo
from . import view


class Giocatore:
    def __init__(self) -> None:
        self.mazzetto = mazzo.Mazzetto()
        self.mano: typing.Optional[mano.Mano] = None

    def gioca(self, terra: typing.List[carta.Carta]) -> None:
        if self.mano is None:
            raise AttributeError()

        if len(self.mano) == 1:
            i = 0
        else:
            view.pprint('[giocatore: %s] carte in mano: %s, carte a terra: %s', self, self.mano, terra)
            s = input('scegli una carta: ')
            while s not in map(str, range(1, len(self.mano)+1)):
                print('inserisci un numero tra 1 e %s' % (len(self.mano)+1))
                s = input('scegli una carta: ')
            i = int(s) - 1
        c = self.mano.pop(i)
        self.prendi(c, terra)

    def prendi(self,
               c: carta.Carta,
               terra: typing.List[carta.Carta]) -> None:
        # se c'è almeno una carta con il valore di quella che hai giocato, prendila
        stesso_valore = [t for t in terra if t.valore == c.valore]

        # preferisci i denari
        if len(stesso_valore) >= 1:
            def preferisci_denari(c: carta.Carta) -> int:
                if c.seme == carta.Seme.denari:
                    return 2
                else:
                    return 1
            self._prendi(c, sorted(stesso_valore, key=preferisci_denari)[:1], terra)
            return

        # prova tutte le combinazioni di carte < c, vedi se ce n'è qualcuna la cui somma è c
        carte_basse = [t for t in terra if t.valore < c.valore]

        # preferisci combinazioni lunghe
        for r in range(len(carte_basse), 1, -1):
            for comb in itertools.combinations(carte_basse, r):
                if sum(t.valore for t in comb) == c.valore:
                    # found!
                    self._prendi(c, comb, terra)
                    return

        view.pprint("[giocatore: %s] non so prendere... aggiungo %s a %s", self, c, terra)
        terra.append(c)

    def _prendi(self,
                c: carta.Carta,
                comb: typing.Sequence[carta.Carta],
                terra: typing.List[carta.Carta]) -> None:
        view.pprint("[giocatore: %s] prendo %s da %s con un %s!", self, comb, terra, c)
        # tolgo le carte da terra
        for t in comb:
            terra.remove(t)

        # le metto sul mio mazzetto, con la carta che ho usato
        self.mazzetto.extend(comb)
        self.mazzetto.append(c)

        # scopa!
        if not terra:
            c.retro = True

    def __str__(self) -> str:
        return 'TU'


class Partita:
    def __init__(self, *giocatori: Giocatore):
        self.giocatori = giocatori

        # creazione mondo
        self.mazzo = mazzo.Mazzo()
        self.mazzo.mischia()
        self.gioca(prima_volta=True)

    def gioca(self, prima_volta: bool=False) -> None:
        # distribuzione carte - la prima volta con le carte a terra
        for i, giocatore in enumerate(self.giocatori):
            # al cartaro va dopo aver messo le carte a terra
            if i != len(self.giocatori) - 1:
                giocatore.mano = mano.Mano(*self.mazzo.carte(3))
        if prima_volta:
            self.terra = self.mazzo.carte(4)
            view.pprint("terra: %s", self.terra)
        self.giocatori[-1].mano = mano.Mano(*self.mazzo.carte(3))

        # i 3 turni delle 3 carte in mano
        for _ in range(3):
            for giocatore in self.giocatori:
                giocatore.gioca(terra=self.terra)   # modifica terra in-place

        # se è finito il mazzo, vai a calcolare i punti, altrimenti altro giro
        if self.mazzo:
            self.gioca()
        else:
            self.punti()

    def punti(self) -> None:
        for giocatore in self.giocatori:
            altri_giocatori = set(self.giocatori) - set([giocatore])
            altre_mani = [g.mazzetto for g in altri_giocatori]
            print(giocatore.mazzetto.punti(*altre_mani))


class AI(Giocatore):
    def __init__(self, i: str) -> None:
        super().__init__()
        self.i = i

    def gioca(self, terra: typing.List[carta.Carta]) -> None:
        if self.mano is None:
            raise AttributeError()

        c = random.choice(self.mano)
        self.prendi(c, terra)

    def __str__(self) -> str:
        return 'Ai-' + self.i


def main() -> None:
    Partita(Giocatore(), AI('2'), AI('3'), AI('4'))
