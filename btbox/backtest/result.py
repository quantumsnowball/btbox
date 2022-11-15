from btbox.broker.report import Report
from btbox.strategy import Strategy


class Result:
    def __init__(self,
                 strategy: Strategy,
                 report: Report):
        self._strategy = strategy
        self._report = report

    @property
    def report(self) -> Report:
        return self._report

    def plot(self):
        self._report.nav.plot()
