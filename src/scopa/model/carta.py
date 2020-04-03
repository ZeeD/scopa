'a simple card'

import dataclasses
import enum


class Seme(enum.Enum):
    'the cards suits'
    denari = 1
    coppe = 2
    bastoni = 3
    spade = 4

    def __str__(self) -> str:
        return self.name


class Valore(enum.IntEnum):
    'the cards values'
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


@dataclasses.dataclass
class Carta:
    'a simple model for a card'

    seme: Seme
    valore: Valore
    retro: bool = False

    def __str__(self) -> str:
        return '"%s di %s"' % (self.valore, self.seme)
