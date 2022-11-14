from btbox.market import Market


class Backtest:
    def __init__(self, strategy, market):
        self._strategy = strategy
        self._market = market

    def run(self):
        self._strategy.run()


# helper
def create(Strategy, data):
    strategy = Strategy()
    market = Market(data)
    backtest = Backtest(strategy, market)
    return backtest
