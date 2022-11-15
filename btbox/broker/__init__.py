from btbox.broker.account import Account
from btbox.broker.audit import Audit
from btbox.broker.report import Report
from btbox.market import Market
from datetime import datetime
from typing import List


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
    def report(self) -> Report:
        return self._report
    # system

    def sync(self, now) -> None:
        self._now = now
        # set now attr to a new timestamp in market
        self._market.sync(now)

    # operations
    def deposit(self,
                amount: float) -> None:
        self._account.cash += amount

    def trade(self,
              ticker: str,
              amount: float) -> None:
        pass

    # audit
    def settlement(self) -> None:
        # write nav history
        nav = self._audit.nav_account()
        self._report.log_nav_history(self._now, nav)
