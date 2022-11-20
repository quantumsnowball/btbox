from collections.abc import Callable
from btbox.backtest.results.selected.journals import Journals
from btbox.backtest.results.selected.nav import Nav
from btbox.broker.report import Report
from btbox.strategy import Strategy


class Selected:
    def __init__(self,
                 name: str,
                 strategy: Strategy,
                 report: Report) -> None:
        self._name = name
        self._strategy = strategy
        self._report = report
        self._nav = Nav(self._name, self._report.nav)
        self._journals = Journals(self._name, self._strategy.journal)

    @property
    def nav(self) -> Nav:
        return self._nav

    @property
    def journals(self) -> Journals:
        return self._journals

    @property
    def plot(self) -> Callable[..., None]:
        return self._nav.plot
