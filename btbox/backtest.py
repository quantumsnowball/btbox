import pandas as pd
from btbox.datasource import DataSource
from btbox.market import Market
from btbox.strategy import Strategy
from btbox.broker import Broker
from typing import Type, Dict


class Backtest:
    def __init__(self,
                 strategy: Strategy) -> None:
        assert isinstance(strategy, Strategy)
        self._strategy = strategy
        self._broker = self._strategy.broker
        self._timeline = self._strategy.timeline

    def run(self) -> None:
        # timeline loop
        for i, now in enumerate(self._timeline):
            # set now attr to a new timestamp in strategy
            self._strategy.sync(now)
            # run strategy as defined by user
            self._strategy.step(i, now, self._broker)
            # do daily settlement
            self._broker.settlement()


# helper
def create(CustomStrategy: Type[Strategy],
           dataframes: Dict[str, pd.DataFrame]) -> Backtest:
    datasource = DataSource(dataframes)
    market = Market(datasource)
    broker = Broker(market)
    strategy = CustomStrategy(broker)
    backtest = Backtest(strategy)
    return backtest
