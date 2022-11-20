from pandas import DataFrame, concat
import plotly.express as px
from btbox.broker.report import Report
from btbox.strategy import Strategy


class Navs:
    def __init__(self,
                 reports: list[Report],
                 strategies: list[Strategy]) -> None:
        self._reports = reports
        self._strategies = strategies

    @property
    def values(self) -> DataFrame:
        df = concat([r.nav for r in self._reports], axis=1)
        df.columns = [s.name for s in self._strategies]
        return df

    def plot(self, **line_kws) -> None:
        fig = px.line(self.values, **line_kws)
        fig.show()
