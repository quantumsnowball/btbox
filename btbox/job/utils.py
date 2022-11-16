from pandas import DataFrame
from btbox.job import Job
from btbox.share import Clock
from btbox.datasource import DataSource
from btbox.market import Market
from btbox.strategy import Strategy
from btbox.broker import Broker


# helper
def create_job(CustomStrategy: type[Strategy],
               dataframes: dict[str, DataFrame],
               **kwds_DataSource) -> Job:
    clock = Clock()
    datasource = DataSource(dataframes, **kwds_DataSource)
    market = Market(datasource, clock)
    broker = Broker(market, clock)
    strategy = CustomStrategy(broker, clock)
    job = Job(strategy, clock)
    return job
