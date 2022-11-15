from btbox.broker.account import Account
from btbox.broker.audit import Audit
from btbox.broker.report import Report
from btbox.market import Market
from datetime import datetime
from typing import List, Dict


class Broker:
    def __init__(self,
                 market: Market) -> None:
        self._market = market
        self._timeline = self._market.timeline
        self._account = Account()
        self._audit = Audit(self._market, self._account)
        self._report = Report()

    @property
    def timeline(self) -> List[datetime]:
        return self._timeline

    @property
    def cash(self) -> float:
        return self._account.cash

    @property
    def positions(self) -> Dict[str, float]:
        return self._account.positions

    @property
    def report(self) -> Report:
        return self._report

    @property
    def audit(self) -> Audit:
        return self._audit

    @property
    def market(self) -> Market:
        return self._market

    # system
    def sync(self, now) -> None:
        self._now = now
        # set now attr to a new timestamp in market
        self._market.sync(now)
        self._audit.sync(now)

    # operations
    def deposit(self,
                amount: float) -> None:
        self._account.cash += amount

    def withdrawal(self,
                   amount: float) -> None:
        self._account.cash -= amount

    def trade(self,
              symbol: str,
              quantity: float) -> None:
        # price
        price = self._market.get_close_at(symbol, self._now)
        # cash flow
        gross_proceeds = -price * quantity
        fees = 0
        net_proceeds = gross_proceeds - fees
        # settlement
        self._account.cash += net_proceeds
        self._account.positions[symbol] += quantity
        # write trade history
        self._report.log_trade(
            date=self._now, symbol=symbol,
            action='BOT' if quantity >= 0 else 'SLD', quantity=quantity,
            price=price, gross_proceeds=gross_proceeds, fees=fees,
            net_proceeds=net_proceeds)

    # audit
    def settlement(self) -> None:
        # write nav history
        nav = self._audit.nav_account()
        self._report.log_nav(self._now, nav)
