from datetime import datetime
from typing import List, Tuple
import pandas as pd


class _Record:
    class NavHistory:
        columns = ('Date', 'NAV')
        type = Tuple[datetime, float]

    class TradeHistory:
        columns = 'Date Symbol Action Quantity Price GrossProceeds Fees NetProceeds'.split(
            ' ')
        # type = TODO


class Report:
    def __init__(self) -> None:
        self._nav_history_log: List[_Record.NavHistory.type] = []

    @property
    def nav_history(self) -> pd.Series:
        df = pd.DataFrame(self._nav_history_log,
                          columns=_Record.NavHistory.columns)
        return pd.Series(df.NAV.values,
                         index=df.Date,
                         name=_Record.NavHistory.columns[-1])

    def log_nav_history(self, date: datetime, nav: float) -> None:
        self._nav_history_log.append((date, nav, ))
