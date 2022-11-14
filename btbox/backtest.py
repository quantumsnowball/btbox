class Backtest:
    def __init__(self, strategy):
        self._strategy = strategy

    def run(self):
        self._strategy.run()


def create(Strategy):
    strategy = Strategy()
    backtest = Backtest(strategy)
    return backtest
