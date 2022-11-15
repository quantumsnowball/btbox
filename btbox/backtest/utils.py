from pandas import DataFrame
from btbox.backtest import Backtest
from btbox.clock import Clock
from btbox.datasource import DataSource
from btbox.market import Market
from btbox.strategy import Strategy
from btbox.broker import Broker
from typing import Type, Dict


# helper
def create(CustomStrategy: Type[Strategy],
           dataframes: Dict[str, DataFrame]) -> Backtest:
    clock = Clock()
    datasource = DataSource(dataframes)
    market = Market(datasource, clock)
    broker = Broker(market, clock)
    strategy = CustomStrategy(broker, clock)
    backtest = Backtest(strategy, clock)
    return backtest
