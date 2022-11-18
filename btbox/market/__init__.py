from pandas import DataFrame
from datetime import datetime
from btbox.share import Clock
from btbox.datasource import DataSource
from functools import cache


class Market:
    def __init__(self,
                 datasource: DataSource,
                 clock: Clock) -> None:
        self._datasource = datasource
        self._timeline = self._datasource.timeline
        self._clock = clock

    @property
    def timeline(self) -> list[datetime]:
        return self._timeline
