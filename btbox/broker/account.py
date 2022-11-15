from typing import Dict


class Account:
    def __init__(self) -> None:
        self._cash: float = 0
        self._positions: Dict[str, float] = {}

    # cash
    @property
    def cash(self) -> float:
        return self._cash

    @cash.setter
    def cash(self, cash: float) -> None:
        self._cash = cash

    # positions
    @property
    def positions(self) -> Dict[str, float]:
        return self._positions
