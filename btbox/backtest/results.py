from typing import List
from btbox.broker.report import Report
from btbox.job.result import Result
from pandas import DataFrame, concat
import plotly.express as px

from btbox.strategy import Strategy


class Results:
    def __init__(self,
                 results: List[Result]) -> None:
        self._strategies = [r.strategy for r in results]
        self._reports = [r.report for r in results]

    @property
    def strategies(self) -> List[Strategy]:
        return self._strategies

    @property
    def reports(self) -> List[Report]:
        return self._reports

    @property
    def navs(self) -> DataFrame:
        df = concat([r.nav for r in self._reports], axis=1)
        df.columns = [s.name for s in self._strategies]
        return df

    def plot(self, **line_kws):
        fig = px.line(self.navs, **line_kws)
        fig.show()
