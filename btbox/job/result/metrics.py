from functools import cached_property
import pandas as pd
import numpy as np
from pandas import Series, DataFrame
from btbox.broker.report import Report
from btbox.strategy import Strategy


def detect_annualize_factor(ts: Series | DataFrame,
                            sample_size: int = 100) -> float:

    def cal_annualize_factor(ts: Series | DataFrame) -> float:
        timeline = ts.index
        time_diff = (timeline[-1] - timeline[0])
        year_diff = time_diff.total_seconds() / 60 / 60 / 24 / 365.25
        n_timeline = len(timeline) - 1
        annualize_factor = n_timeline / year_diff
        return annualize_factor

    N = len(ts)
    len_trunk = min(N, sample_size)
    trunks = [trunk
              for i in range(-1, -N - 1, -len_trunk)
              if len(trunk := ts.iloc[i - len_trunk: i]) >= len_trunk * 0.9]
    stats = [cal_annualize_factor(trunk)
             for trunk in trunks]
    median = np.median(stats)
    assert isinstance(median, float)
    return median


def total_return(ts: Series) -> float:
    ans = ts.iloc[-1] / ts.iloc[0] - 1
    return ans


def cagr(ts: Series) -> float:
    ydiff = (ts.index[-1] - ts.index[0]) / pd.Timedelta(days=365)
    ans = (ts.iloc[-1] / ts.iloc[0]) ** (1 / ydiff) - 1
    return ans


def mu_sigma(ts: Series,
             annualize_factor: float) -> tuple[float, float]:
    chgs = ts.pct_change()
    mean = chgs.mean()
    std = chgs.std()
    assert isinstance(mean, float)
    assert isinstance(std, float)
    mu = mean * annualize_factor
    sigma = std * annualize_factor**0.5
    return mu, sigma


def sharpe(ts: Series,
           annualize_factor: float,
           riskfree: float) -> float:
    mu, sigma = mu_sigma(ts, annualize_factor)
    sharpe = (mu - riskfree) / sigma
    return sharpe


class Metrics:
    def __init__(self,
                 strategy: Strategy,
                 report: Report) -> None:
        self._strategy = strategy
        self._report = report

    @cached_property
    def total_return(self) -> float:
        return total_return(self._report.nav)

    @cached_property
    def cagr(self) -> float:
        return cagr(self._report.nav)

    @cached_property
    def mu_sigma(self) -> float:
        annualize_factor = 252
        return mu_sigma(self._report.nav, annualize_factor)
