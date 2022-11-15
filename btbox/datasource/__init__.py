from pandas import read_csv, DataFrame
from datetime import datetime
from typing import Dict, List
from functools import cache
from btbox.datasource.utils import verify_ohlcv


class DataSource:
    def __init__(self,
                 dataframes: Dict[str, DataFrame],
                 window: int = 1) -> None:
        for df in dataframes.values():
            verify_ohlcv(df)
        self._dataframes = dataframes
        self._window = window
        self._timeline = list(self._dataframes.values())[0].index.to_list()

    @property
    def timeline(self) -> List[datetime]:
        return self._timeline

    @cache
    def get_ohlcv(self, symbol: str) -> DataFrame:
        return self._dataframes[symbol]

    # helper
    @classmethod
    def import_yahoo_csv(cls, path: str) -> DataFrame:
        df = read_csv(path,
                      index_col='Date',
                      parse_dates=True)
        df.drop('Close', axis=1, inplace=True)
        df.rename({'Adj Close': 'Close'}, axis=1, inplace=True)
        return df
