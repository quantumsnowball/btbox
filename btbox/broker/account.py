from collections import defaultdict


class Account:
    def __init__(self) -> None:
        self._cash: float = 0
        self._positions: dict[str, float] = defaultdict(float)

    # cash
    @property
    def cash(self) -> float:
        return self._cash

    @cash.setter
    def cash(self, cash: float) -> None:
        self._cash = cash

    # positions
    @property
    def positions(self) -> dict[str, float]:
        return self._positions
