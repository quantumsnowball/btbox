from typing import Any
from pandas import DataFrame, concat
import plotly.express as px
from btbox.broker.report import Report
from btbox.strategy import Strategy


class Navs:
    def __init__(self,
                 reports: dict[str, Report],
                 strategies: dict[str, Strategy]) -> None:
        self._reports = reports
        self._strategies = strategies

    @property
    def values(self) -> DataFrame:
        df = concat([r.nav for r in self._reports.values()], axis=1)
        df.columns = self._strategies.keys()
        return df

    def plot(self, **kwargs_line: Any) -> None:
        fig = px.line(self.values, **kwargs_line)
        fig.show()
