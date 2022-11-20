from typing import Callable
from pandas.io.formats.style import Styler
from btbox.backtest.results.navs import Navs
from btbox.broker.report import Report
from btbox.job.result import Result
from pandas import DataFrame
from btbox.job.result.metrics import Metrics
from btbox.strategy import Strategy


class Results:
    def __init__(self,
                 results: list[Result]) -> None:
        self._results = results
        self._strategies = [r.strategy for r in self._results]
        self._reports = [r.report for r in self._results]
        self._metrics = list(r.metrics for r in self._results)
        self._navs = Navs(self._reports, self._strategies)

    @property
    def results(self) -> list[Result]:
        return self._results

    @property
    def strategies(self) -> list[Strategy]:
        return self._strategies

    @property
    def reports(self) -> list[Report]:
        return self._reports

    @property
    def metrics(self) -> list[Metrics]:
        return self._metrics

    @property
    def navs(self) -> Navs:
        return self._navs

    @property
    def plot(self) -> Callable[..., None]:
        return self._navs.plot

    def dashboard(self) -> DataFrame:
        names = [s.name for s in self._strategies]
        data = {
            'return': [m.total_return for m in self._metrics],
            'cagr': [m.cagr for m in self._metrics],
            'mu': [m.mu_sigma[0] for m in self._metrics],
            'sigma': [m.mu_sigma[1] for m in self._metrics],
            'mdd': [m.drawdown.maxdrawdown for m in self._metrics],
            'duration': [m.drawdown.duration for m in self._metrics],
            'sharpe': [m.sharpe for m in self._metrics],
            'calmar': [m.calmar for m in self._metrics]
        }
        df = DataFrame(data, index=names)
        return df

    def dashboard_pretty(self) -> Styler:
        raw = self.dashboard()
        pretty = raw.style.format({
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
