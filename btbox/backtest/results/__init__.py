from functools import cache
from typing import Callable
from pandas.io.formats.style import Styler
from btbox.backtest.results.navs import Navs
from btbox.backtest.results.selected import Selected
from btbox.broker.report import Report
from btbox.job.result import Result
from pandas import DataFrame
from btbox.job.result.metrics import Metrics
from btbox.strategy import Strategy


class Results:
    def __init__(self,
                 results: list[Result]) -> None:
        self._results = {r.name: r for r in results}
        self._strategies = {n: r.strategy for n, r in self._results.items()}
        self._reports = {n: r.report for n, r in self._results.items()}
        self._metrics = {n: r.metrics for n, r in self._results.items()}
        self._navs = Navs(self._reports, self._strategies)

    @cache
    def __getitem__(self, name: str) -> Selected:
        strategy = self._strategies[name]
        result = self._results[name]
        return Selected(name, strategy, result)

    @property
    def results(self) -> dict[str, Result]:
        return self._results

    @property
    def strategies(self) -> dict[str, Strategy]:
        return self._strategies

    @property
    def reports(self) -> dict[str, Report]:
        return self._reports

    @property
    def metrics(self) -> dict[str, Metrics]:
        return self._metrics

    @property
    def navs(self) -> Navs:
        return self._navs

    @property
    def plot(self) -> Callable[..., None]:
        return self._navs.plot

    def dashboard(self) -> DataFrame:
        names = list(self._strategies)
        data = {
            'return': [m.total_return for m in self._metrics.values()],
            'cagr': [m.cagr for m in self._metrics.values()],
            'mu': [m.mu_sigma[0] for m in self._metrics.values()],
            'sigma': [m.mu_sigma[1] for m in self._metrics.values()],
            'mdd': [m.drawdown.maxdrawdown for m in self._metrics.values()],
            'duration': [m.drawdown.duration for m in self._metrics.values()],
            'sharpe': [m.sharpe for m in self._metrics.values()],
            'calmar': [m.calmar for m in self._metrics.values()]
        }
        df = DataFrame(data, index=names)
        return df

    def dashboard_pretty(self) -> Styler:
        raw = self.dashboard()
        pretty: Styler = raw.style.format({
            'return': '{:,.1%}',
            'cagr': '{:.2%}',
            'mu': '{:.2%}',
            'sigma': '{:.2%}',
            'mdd': '{:.2%}',
            'duration': lambda d: str(d)[:-3],
            'sharpe': '{:.3f}',
            'calmar': '{:.3f}',
        })
        return pretty
