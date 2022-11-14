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
def create(Strategy: Type[Strategy],
           data: pd.DataFrame) -> Backtest:
    strategy = Strategy()
    market = Market(data)
    broker = Broker()
    backtest = Backtest(strategy, market, broker)
    return backtest
