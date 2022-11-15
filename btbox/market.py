import pandas as pd
from datetime import datetime
from btbox.datasource import DataSource
from typing import List


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

    def get_ohlcv_at(self,
                     symbol: str,
                     at: datetime) -> pd.DataFrame:
        return pd.DataFrame()

    def get_close_at(self,
                     symbol: str,
                     at: datetime) -> float:
        return 350

    def get_ohlcv_window_at(self, symbol: str, at: datetime, length: int) -> pd.DataFrame:
        return pd.DataFrame()
