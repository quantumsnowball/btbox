from datetime import datetime
from btbox.share import Clock
from btbox.broker import Broker


class Strategy:
    name: str = 'UnnamedStrategy'

    def __init__(self,
                 broker: Broker,
                 clock: Clock) -> None:
        self._broker = broker
        self._timeline = self._broker.timeline
        self._clock = clock

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
