from abc import ABC, abstractmethod
from datetime import datetime
from typing import List
from btbox.clock import Clock
from btbox.broker import Broker


class Strategy(ABC):
    name: str = 'UnnamedStrategy'

    def __init__(self,
                 broker: Broker,
                 clock: Clock) -> None:
        self._broker = broker
        self._timeline = self._broker.timeline
        self._clock = clock

    @property
    def timeline(self) -> List[datetime]:
        return self._timeline

    @property
    def broker(self) -> Broker:
        return self._broker

    @abstractmethod
    def step(self,
             i: int,
             now: datetime,
             broker: Broker) -> None:
        pass
