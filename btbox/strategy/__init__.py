from datetime import datetime
from btbox.share import Clock
from btbox.broker import Broker
from btbox.strategy.journal import Journal


DEFAULT_CAPITAL = 1e6


class Strategy:
    name: str = ''
    capital: float = DEFAULT_CAPITAL

    def __init__(self,
                 broker: Broker,
                 clock: Clock) -> None:
        if len(self.name) == 0:
            self.name = self.__class__.__name__
        self._broker = broker
        self._timeline = self._broker.timeline
        self._clock = clock
        self._journal = Journal(self._clock, self._timeline)
        self._broker.order.deposit(self.capital)

    @property
    def timeline(self) -> list[datetime]:
        return self._timeline

    @property
    def broker(self) -> Broker:
        return self._broker

    @property
    def journal(self) -> Journal:
        return self._journal

    def initial(self,
                b: Broker) -> None:
        pass

    def step(self,
             i: int,
             b: Broker) -> None:
        pass
