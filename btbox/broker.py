from typing import Dict
from btbox.market import Market
from datetime import datetime
from typing import List


class Broker:
    def __init__(self,
                 market: Market) -> None:
        self._market = market
        self._timeline = self._market.timeline
        self._cash: float = 0
        self._positions: Dict[str, float] = {}

    @property
    def timeline(self) -> List[datetime]:
        return self._timeline

    @property
    def cash(self) -> float:
        return self._cash

    # system
    def sync(self, now) -> None:
        self._now = now
        # set now attr to a new timestamp in market
        self._market.sync(now)

    # operations
    def deposit(self,
                amount: float) -> None:
        self._cash += amount

    def trade(self,
              ticker: str,
              amount: float) -> None:
        pass

    # audit
    def settlement(self) -> None:
        # write nav history
        nav = self.nav_account()
        pass

    def nav_position(self,
                     position: str) -> float:
        # TODO
        return 0

    def nav_all_positions(self) -> float:
        value = 0.0
        for position in self._positions:
            value += self.nav_position(position)
        return value

    def nav_account(self) -> float:
        position_value = self.nav_all_positions()
        nav = position_value + self._cash
        return nav
