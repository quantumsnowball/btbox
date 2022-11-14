import pandas as pd
from btbox.datasource import DataSource
from btbox.market import Market
from btbox.strategy import Strategy
from btbox.broker import Broker
from typing import Type


class Backtest:
    def __init__(self,
                 strategy: Strategy):
        assert isinstance(strategy, Strategy)
        self._strategy = strategy
        self._broker = self._strategy.broker

    def run(self):
        # timeline loop
        for i, now in enumerate(timeline):
            # set now attr to a new timestamp in strategy
            self._strategy.sync(now)
            # set now attr to a new timestamp in broker
            self._strategy.broker.sync(now)
            # set now attr to a new timestamp in market
            self._strategy.market.sync(now)
            # run strategy as defined by user
            self._strategy.step(i, now, self._strategy.broker)
            # do daily settlement
            self._strategy.broker.settlement()


# helper
def create(CustomStrategy: Type[Strategy],
           dataframe: pd.DataFrame) -> Backtest:
    datasource = DataSource(dataframe)
    market = Market(datasource)
    broker = Broker(market)
    strategy = CustomStrategy(broker)
    backtest = Backtest(strategy)
    return backtest
