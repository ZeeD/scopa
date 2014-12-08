#!/usr/bin/env python3

import random
import itertools

import model.carta
import model.mazzo
import model.mano
import view

class Partita:
    def __init__(self, *giocatori):
        self.giocatori = giocatori

        # creazione mondo
        self.mazzo = model.mazzo.Mazzo()
        self.mazzo.mischia()
        self.gioca(prima_volta=True)

    def gioca(self, prima_volta=False):
        # distribuzione carte - la prima volta con le carte a terra
        for i, giocatore in enumerate(self.giocatori):
            giocatore.mazzetto = model.mazzo.Mazzetto() # vuoto
            if i != len(self.giocatori) - 1:            # al cartaro va dopo aver messo le carte a terra
                giocatore.mano = model.mano.Mano(*self.mazzo.carte(3))
        if prima_volta:
            self.terra = self.mazzo.carte(4)
            view.pprint("terra: %s", self.terra)
        self.giocatori[-1].mano = model.mano.Mano(*self.mazzo.carte(3))

        # i 3 turni delle 3 carte in mano
        for _ in range(3):
            for giocatore in self.giocatori:
                giocatore.gioca(terra=self.terra)   # modifica terra in-place

        # se è finito il mazzo, vai a calcolare i punti, altrimenti altro giro
        if self.mazzo:
            self.gioca()
        else:
            self.punti()

    def punti(self):
        for giocatore in self.giocatori:
            altri_giocatori = set(self.giocatori) - set([giocatore])
            altre_mani = [ g.mazzetto for g in altri_giocatori ]
            print(giocatore.mazzetto.punti(*altre_mani))

class Giocatore:
    def gioca(self, terra):
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

    def prendi(self, c, terra):
        # se c'è almeno una carta con il valore di quella che hai giocato, prendila
        stesso_valore = [ t for t in terra if t.valore == c.valore ]

        # preferisci i denari
        if len(stesso_valore) >= 1:
            def preferisci_denari(c):
                if c.seme == model.carta.Seme.denari:
                    return 2
                else:
                    return 1
            self._prendi(c, sorted(stesso_valore, key=preferisci_denari)[:1], terra)
            return

        # prova tutte le combinazioni di carte < c, vedi se ce n'è qualcuna la cui somma è c
        carte_basse = [ t for t in terra if t.valore < c.valore ]

        # preferisci combinazioni lunghe
        for r in range(len(carte_basse), 1, -1):
            for comb in itertools.combinations(carte_basse, r):
                if sum(t.valore for t in comb) == c.valore:
                    # found!
                    self._prendi(c, comb, terra)
                    return

        view.pprint("[giocatore: %s] non so prendere... aggiungo %s a %s", self, c, terra)
        terra.append(c)

    def _prendi(self, c, comb, terra):
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

    def __str__(self):
        return 'TU'

class AI(Giocatore):
    def __init__(self, i):
        super().__init__()
        self.i = i

    def gioca(self, terra):
        c = random.choice(self.mano)
        self.prendi(c, terra)

    def __str__(self):
        return 'Ai-' + self.i

def main():
    Partita(Giocatore(), AI('2'), AI('3'), AI('4'))
