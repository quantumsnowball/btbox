from btbox.share import Clock
from btbox.broker.account import Account
from btbox.market import Market


class Audit:
    def __init__(self,
                 market: Market,
                 account: Account,
                 clock: Clock) -> None:
        self._market = market
        self._account = account
        self._clock = clock

    def nav_position(self,
                     symbol: str) -> float:
        price = self._market.get_close(symbol)
        nav = self._account.positions[symbol] * price
        return nav

    def nav_all_positions(self) -> float:
        value = 0.0
        for position in self._account.positions:
            value += self.nav_position(position)
        return value

    def nav_account(self) -> float:
        position_value = self.nav_all_positions()
        nav = position_value + self._account.cash
        return nav
