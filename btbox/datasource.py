import pandas as pd
from datetime import datetime
from typing import List


class DataSource:
    def __init__(self,
                 dataframe: pd.DataFrame,
                 window: int = 1) -> None:
        assert isinstance(dataframe, pd.DataFrame)
        self._dataframe = dataframe
        self._window = window
        self._timeline = self._dataframe.index.to_list()

    @property
    def timeline(self) -> List[datetime]:
        return self._timeline
