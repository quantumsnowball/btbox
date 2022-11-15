from pandas import DataFrame
from btbox.backtest import Backtest
from btbox.datasource import DataSource
from btbox.market import Market
from btbox.strategy import Strategy
from btbox.broker import Broker
from typing import Type, Dict


# helper
def create(CustomStrategy: Type[Strategy],
           dataframes: Dict[str, DataFrame]) -> Backtest:
    datasource = DataSource(dataframes)
    market = Market(datasource)
    broker = Broker(market)
    strategy = CustomStrategy(broker)
    backtest = Backtest(strategy)
    return backtest
