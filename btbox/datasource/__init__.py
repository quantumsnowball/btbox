from pandas import DataFrame
from datetime import datetime
from typing import Dict, List, Union
from functools import cache
from btbox.datasource.utils import (
    parse_start_end_window,
    trim_ohlcv_length,
    verify_ohlcv
)


class DataSource:
    def __init__(self,
                 dataframes: Dict[str, DataFrame],
                 *,
                 start: Union[datetime, str, None] = None,
                 end: Union[datetime, str, None] = None,
                 window: int = 1) -> None:
        (self._start,
         self._end,
         self._window,
         trim_from,
         trim_to) = parse_start_end_window(
            next(iter(dataframes.values())), start, end, window)
        self._dataframes = {
            k: trim_ohlcv_length(df, trim_from, trim_to)
            for k, df in dataframes.items()}
        self._timeline = next(iter(self._dataframes.values())
                              ).loc[self._start:self._end].index.to_list()

    @property
    def timeline(self) -> List[datetime]:
        return self._timeline

    @cache
    def get_ohlcv(self, symbol: str) -> DataFrame:
        return self._dataframes[symbol]
