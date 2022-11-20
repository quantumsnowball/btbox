from collections.abc import Callable
from btbox.backtest.results.selected.nav import Nav
from btbox.broker.report import Report


class Selected:
    def __init__(self,
                 name: str,
                 report: Report) -> None:
        self._name = name
        self._report = report
        self._nav = Nav(self._name, self._report.nav)

    @property
    def nav(self) -> Nav:
        return self._nav

    @property
    def journal(self):
        pass

    @property
    def plot(self) -> Callable[..., None]:
        return self._nav.plot
