from btbox.broker.report import Report
from btbox.strategy import Strategy
import plotly.express as px


class Result:
    def __init__(self,
                 strategy: Strategy,
                 report: Report):
        self._strategy = strategy
        self._report = report

    @property
    def strategy(self) -> Strategy:
        return self._strategy

    @property
    def report(self) -> Report:
        return self._report

    def plot(self, **line_kws) -> None:
        fig = px.line(x=self._report.nav.index,
                      y=self._report.nav,
                      **line_kws)
        fig.show()
