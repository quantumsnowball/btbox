from pandas import DataFrame
from btbox.job import Job
from btbox.clock import Clock
from btbox.datasource import DataSource
from btbox.market import Market
from btbox.strategy import Strategy
from btbox.broker import Broker
from typing import Type, Dict


# helper
def create_job(CustomStrategy: Type[Strategy],
               dataframes: Dict[str, DataFrame]) -> Job:
    clock = Clock()
    datasource = DataSource(dataframes)
    market = Market(datasource, clock)
    broker = Broker(market, clock)
    strategy = CustomStrategy(broker, clock)
    job = Job(strategy, clock)
    return job
