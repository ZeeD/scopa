#!/usr/bin/env python3

import random

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
            print(giocatore.mazzetto.punti(altri_giocatori))

class Giocatore:
    def gioca(self, terra):
        if len(self.mano) == 1:
            i = 0
        else:
            print('[giocatore: %s] carte in mano: %s' % (self, ', '.join(map(str, self.mano))))
            print('carte a terra: ' + ', '.join(map(str, terra)))
            s = input('scegli una carta: ')
            while s not in map(str, range(1, len(self.mano)+1)):
                print('inserisci un numero tra 1 e %s' % (len(self.mano)+1))
                s = input('scegli una carta: ')
            i = int(s) - 1
        carta = self.mano.pop(i)
        self.prendi(carta, terra)

    def prendi(self, carta, terra):
        print("non so prendere... finisce tutto a terra")
        terra.append(carta)

class AI(Giocatore):
    def gioca(self, terra):
        carta = random.choice(self.mano)
        self.prendi(carta, terra)


def main():
    Partita(AI(), AI(), AI(), AI())
