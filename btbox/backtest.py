import pandas as pd
from btbox.market import Market
from btbox.strategy import Strategy
from btbox.broker import Broker
from typing import Type


class Backtest:
    def __init__(self,
                 strategy: Strategy,
                 market: Market,
                 broker: Broker):
        assert isinstance(strategy, Strategy)
        assert isinstance(market, Market)
        assert isinstance(broker, Broker)
        self._strategy = strategy
        self._market = market
        self._broker = broker

    def run(self):
        self._strategy.run()


# helper
def create(Strategy: Type[Strategy],
           data: pd.DataFrame) -> Backtest:
    strategy = Strategy()
    market = Market(data)
    broker = Broker()
    backtest = Backtest(strategy, market, broker)
    return backtest
