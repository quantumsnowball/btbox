from pandas.io.formats.style import Styler
from btbox.broker.report import Report
from btbox.job.result import Result
from pandas import DataFrame, concat
import plotly.express as px
from btbox.job.result.metrics import Metrics

from btbox.strategy import Strategy


class Results:
    def __init__(self,
                 results: list[Result]) -> None:
        self._results = results
        self._strategies = [r.strategy for r in self._results]
        self._reports = [r.report for r in self._results]
        self._metrics = list(r.metrics for r in self._results)

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
    def navs(self) -> DataFrame:
        df = concat([r.nav for r in self._reports], axis=1)
        df.columns = [s.name for s in self._strategies]
        return df

    def plot(self, **line_kws):
        fig = px.line(self.navs, **line_kws)
        fig.show()

    def dashboard(self) -> DataFrame:
        names = [s.name for s in self._strategies]
        data = {
            'return': [m.total_return for m in self._metrics],
            'cagr': [m.cagr for m in self._metrics],
            'mu': [m.mu_sigma[0] for m in self._metrics],
            'sigma': [m.mu_sigma[1] for m in self._metrics],
            'mdd': [m.drawdown.maxdrawdown for m in self._metrics],
            'duration': [m.drawdown.duration for m in self._metrics],
            'sharpe': [m.sharpe for m in self._metrics]
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
            'sharpe': '{:.3f}',
        })
        return pretty
