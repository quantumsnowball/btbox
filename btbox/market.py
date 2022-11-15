import pandas as pd
from datetime import datetime
from btbox.datasource import DataSource
from typing import List
from functools import cache


class Market:
    def __init__(self,
                 datasource: DataSource) -> None:
        self._datasource = datasource
        self._timeline = self._datasource.timeline

    @property
    def timeline(self) -> List[datetime]:
        return self._timeline

    # system
    def sync(self, now) -> None:
        self._now = now

    @cache
    def get_ohlcv_at(self,
                     symbol: str,
                     at: datetime) -> pd.DataFrame:
        return self._datasource.get_ohlcv(symbol).loc[at]

    @cache
    def get_close_at(self,
                     symbol: str,
                     at: datetime) -> float:
        return self._datasource.get_ohlcv(symbol).at[at, 'Close']

    @cache
    def get_ohlcv_window_at(self, symbol: str, at: datetime, length: int) -> pd.DataFrame:
        return pd.DataFrame()
