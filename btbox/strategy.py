from abc import abstractmethod
from datetime import datetime
from btbox.broker import Broker


class Strategy:
    name: str = 'UnnamedStrategy'

    def __init__(self,
                 broker: Broker) -> None:
        self._broker = broker

    @property
    def broker(self):
        return self._broker

    def sync(self,
             now: datetime) -> None:
        self._now = now

    @abstractmethod
    def step(self,
             i: int,
             now: datetime,
             broker: Broker):
        pass
