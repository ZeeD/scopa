import enum

class Seme(enum.Enum):
    denari = 1
    coppe = 2
    bastoni = 3
    spade = 4

    def __str__(self) -> str:
        return self.name


class Valore(enum.IntEnum):
    asso = 1
    due = 2
    tre = 3
    quattro = 4
    cinque = 5
    sei = 6
    sette = 7
    donna = 8
    cavallo = 9
    re = 10

    def __str__(self) -> str:
        return self.name


class Carta:
    def __init__(self, *, seme: Seme, valore: Valore, retro: bool=False) -> None:
        self.seme = seme
        self.valore = valore
        self.retro = retro

    def __str__(self) -> str:
        return '"%s di %s"' % (self.valore, self.seme)
