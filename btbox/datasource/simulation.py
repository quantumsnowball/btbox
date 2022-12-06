from datetime import datetime
import numpy as np
from pandas import DataFrame, DatetimeIndex, date_range


def cal_annualize_factor(timeline: DatetimeIndex) -> float:
    time_diff = (timeline[-1] - timeline[0])
    year_diff = time_diff.total_seconds() / 60 / 60 / 24 / 365.25
    n_timeline = len(timeline) - 1
    annualize_factor = n_timeline / year_diff
    return float(annualize_factor)


def make_random_ohlcv(
    start: datetime | str,
    end: datetime | str,
    freq: str = '1d',
    *,
    p0: float = 100,
    mu: float = 0.0,
    sigma: float = 0.10,
    max_vol_per_period: int = 1000000,
) -> DataFrame:
    dates = date_range(start, end, freq=freq).rename('Date')
    n = len(dates)
    annualize_factor = cal_annualize_factor(dates)
    mean = mu / annualize_factor
    std = sigma / np.sqrt(annualize_factor)
    logdiff = np.random.normal(mean, std, n - 1)
    cumlogdiff = np.cumsum(np.concatenate((np.array([0]), logdiff)))
    pr = p0 * np.exp(cumlogdiff)
    vol = np.random.random(n) * max_vol_per_period
    df = DataFrame(dict(Open=pr, High=pr, Low=pr,
                   Close=pr, Volume=vol), index=dates)
    return df
