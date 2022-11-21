from datetime import datetime
from pandas import DataFrame, DatetimeIndex
from btbox.share import Clock


class Journal:
    def __init__(self,
                 clock: Clock,
                 timeline: DatetimeIndex) -> None:
        self._clock = clock
        self._timeline = timeline
        self._data: dict[datetime, dict[str, float | int | bool | None]] = {}

    @property
    def marks(self) -> DataFrame:
        df = DataFrame(self._data, columns=self._timeline).T
        return df

    def mark(self,
             ind: float | int | bool | None,
             name: str) -> None:
        entry = self._data.get(self._clock.now, {})
        entry[name] = ind
        self._data[self._clock.now] = entry
