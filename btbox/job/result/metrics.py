from functools import cached_property
import pandas as pd
from pandas import Series
from btbox.broker.report import Report
from btbox.strategy import Strategy


def total_return(ts: Series) -> float:
    ans = ts.iloc[-1] / ts.iloc[0] - 1
    return ans


def cagr(ts: Series) -> float:
    ydiff = (ts.index[-1] - ts.index[0]) / pd.Timedelta(days=365)
    ans = (ts.iloc[-1] / ts.iloc[0]) ** (1 / ydiff) - 1
    return ans


class Metrics:
    def __init__(self,
                 strategy: Strategy,
                 report: Report) -> None:
        self._strategy = strategy
        self._report = report

    @cached_property
    def total_return(self) -> float:
        return total_return(self._report.nav)
