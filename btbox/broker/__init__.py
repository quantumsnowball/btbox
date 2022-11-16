from btbox.share import Clock
from btbox.broker.account import Account
from btbox.broker.audit import Audit
from btbox.broker.order import Order
from btbox.broker.portfolio import Portfolio
from btbox.broker.report import Report
from btbox.market import Market
from datetime import datetime
from typing import List, Dict


class Broker:
    def __init__(self,
                 market: Market,
                 clock: Clock) -> None:
        self._market = market
        self._timeline = self._market.timeline
        self._account = Account()
        self._audit = Audit(
            self._market, self._account, clock)
        self._report = Report()
        self._order = Order(
            self._market, self._account, self._report, clock)
        self._portfolio = Portfolio(
            self._order, self._market, self._audit, clock)
        self._clock = clock

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
    def order(self) -> Order:
        return self._order

    @property
    def report(self) -> Report:
        return self._report

    @property
    def audit(self) -> Audit:
        return self._audit

    @property
    def portfolio(self) -> Portfolio:
        return self._portfolio

    @property
    def market(self) -> Market:
        return self._market

    def settlement(self) -> None:
        # write nav history
        nav = self._audit.nav_account()
        self._report.log_nav(self._clock.now, nav)
