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
