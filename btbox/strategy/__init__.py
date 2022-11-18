from datetime import datetime
from btbox.share import Clock
from btbox.broker import Broker


DEFAULT_CAPITAL = 1e6


class Strategy:
    name: str | None = None
    capital: float = DEFAULT_CAPITAL

    def __init__(self,
                 broker: Broker,
                 clock: Clock) -> None:
        if not self.name:
            self.name = self.__class__.__name__
        self._broker = broker
        self._timeline = self._broker.timeline
        self._clock = clock
        self._broker.order.deposit(self.capital)

    @property
    def timeline(self) -> list[datetime]:
        return self._timeline

    @property
    def broker(self) -> Broker:
        return self._broker

    def initial(self,
                b: Broker) -> None:
        pass

    def step(self,
             i: int,
             b: Broker) -> None:
        pass
