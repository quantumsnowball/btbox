from typing import Any
from btbox.broker.report import Report
from btbox.job.result.metrics import Metrics
from btbox.strategy import Strategy
import plotly.express as px


class Result:
    def __init__(self,
                 strategy: Strategy,
                 report: Report):
        self._strategy = strategy
        self._name = strategy.name
        self._report = report
        self._metrics = Metrics(self._strategy, self._report)

    @property
    def name(self) -> str:
        return self._name

    @property
    def strategy(self) -> Strategy:
        return self._strategy

    @property
    def report(self) -> Report:
        return self._report

    @property
    def metrics(self) -> Metrics:
        return self._metrics

    def plot(self, **kwargs_line: Any) -> None:
        fig = px.line(x=self._report.nav.index,
                      y=self._report.nav,
                      **kwargs_line)
        fig.show()
