from btbox.market import Market
from btbox.strategy import Strategy
from btbox.broker import Broker


class Backtest:
    def __init__(self, strategy, market, broker):
        assert isinstance(strategy, Strategy)
        assert isinstance(market, Market)
        assert isinstance(broker, Broker)
        self._strategy = strategy
        self._market = market

    def run(self):
        self._strategy.run()


# helper
def create(Strategy, data):
    strategy = Strategy()
    market = Market(data)
    broker = Broker()
    backtest = Backtest(strategy, market, broker)
    return backtest
