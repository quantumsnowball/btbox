from typing import List
from abc import abstractmethod
from datetime import datetime
from btbox.broker import Broker
from btbox.market import Market


class Strategy:
    name: str = 'UnnamedStrategy'

    def __init__(self,
                 market: Market,
                 broker: Broker,
                 timeline: List[datetime],
                 fund: float = 1e6) -> None:
        self._broker = broker
        self._market = market
        self._timeline = timeline

    def sync(self,
             now: datetime) -> None:
        self._now = now

    @abstractmethod
    def step(self,
             i: int,
             now: datetime,
             broker: Broker):
        pass
