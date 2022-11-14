import pandas as pd
from typing import List
from datetime import datetime


class Market:
    def __init__(self,
                 data: pd.DataFrame) -> None:
        # check
        assert isinstance(data, pd.DataFrame)
        self._data = data
        self._timeline = self._data.index

    @property
    def timeline(self) -> List[datetime]:
        return self._timeline.to_list()
