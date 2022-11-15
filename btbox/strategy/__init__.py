from abc import ABC, abstractmethod
from datetime import datetime
from typing import List
from btbox.broker import Broker


class Strategy(ABC):
    name: str = 'UnnamedStrategy'

    def __init__(self,
                 broker: Broker) -> None:
        self._broker = broker
        self._timeline = self._broker.timeline

    @property
    def timeline(self) -> List[datetime]:
        return self._timeline

    @property
    def broker(self) -> Broker:
        return self._broker

    def sync(self,
             now: datetime) -> None:
        self._now = now
        # set now attr to a new timestamp in broker
        self._broker.sync(now)

    @abstractmethod
    def step(self,
             i: int,
             now: datetime,
             broker: Broker) -> None:
        pass
