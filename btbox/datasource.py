import pandas as pd
from datetime import datetime
from typing import Dict, List


class DataSource:
    def __init__(self,
                 dataframes: Dict[str, pd.DataFrame],
                 window: int = 1) -> None:
        self._dataframes = dataframes
        self._window = window
        self._timeline = list(self._dataframes.values())[0].index.to_list()

    @property
    def timeline(self) -> List[datetime]:
        return self._timeline

    def get_ohlcv(self, symbol: str) -> pd.DataFrame:
        return self._dataframes[symbol]

    # helper
    @classmethod
    def import_yahoo_csv(cls, path: str) -> pd.DataFrame:
        df = pd.read_csv(path,
                         index_col='Date',
                         parse_dates=True)
        return df
