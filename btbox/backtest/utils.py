from typing import Any
from pandas import DataFrame
from btbox.backtest import Backtest
from btbox.job.utils import create_job
from btbox.strategy import Strategy


def create_backtest(CustomStrategys: list[type[Strategy]],
                    dataframes: dict[str, DataFrame],
                    **kwds_create_job: Any) -> Backtest:
    jobs = [create_job(CustomStrategy, dataframes, **kwds_create_job)
            for CustomStrategy in CustomStrategys]
    backtest = Backtest(jobs)
    return backtest
