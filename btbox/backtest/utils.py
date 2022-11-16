from typing import Dict, List, Type
from pandas import DataFrame
from btbox.backtest import Backtest
from btbox.job.utils import create_job
from btbox.strategy import Strategy


def create_backtest(CustomStrategys: List[Type[Strategy]],
                    dataframes: Dict[str, DataFrame]) -> Backtest:
    jobs = [create_job(CustomStrategy, dataframes)
            for CustomStrategy in CustomStrategys]
    backtest = Backtest(jobs)
    return backtest
