from pandas import DataFrame, DatetimeIndex, Series
from btbox.share import Clock
from btbox.datasource import DataSource


class Market:
    def __init__(self,
                 datasource: DataSource,
                 clock: Clock) -> None:
        self._datasource = datasource
        self._timeline = self._datasource.timeline
        self._clock = clock

    @property
    def timeline(self) -> DatetimeIndex:
        return self._timeline

    def get_ohlcv(self,
                  symbol: str) -> DataFrame:
        return self._datasource.get_ohlcv_at(symbol,
                                             self._clock.now)

    def get_close(self,
                  symbol: str) -> float:
        return self._datasource.get_close_at(symbol,
                                             self._clock.now)

    def get_ohlcv_window(self,
                         symbol: str) -> DataFrame:
        return self._datasource.get_ohlcv_window_at(symbol,
                                                    self._clock.now)

    def get_close_window(self,
                         symbol: str) -> Series:
        return self._datasource.get_close_window_at(symbol,
                                                    self._clock.now)
