import typing

from . import carta

class Mano(typing.List[carta.Carta]):
    def __init__(self, *carte: carta.Carta) -> None:
        super().__init__()
        self.extend(carte)
