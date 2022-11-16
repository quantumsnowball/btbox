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

    @cache
    def get_ohlcv_at(self,
                     symbol: str,
                     at: datetime) -> DataFrame:
        return self._datasource.get_ohlcv(symbol).loc[at]

    @cache
    def get_close_at(self,
                     symbol: str,
                     at: datetime) -> float:
        return self._datasource.get_ohlcv(symbol).at[at, 'Close']

    @cache
    def get_ohlcv_window_at(self,
                            symbol: str,
                            on: datetime,
                            length: int) -> DataFrame:
        return self._datasource.get_ohlcv(symbol).loc[:on].iloc[-length:]
