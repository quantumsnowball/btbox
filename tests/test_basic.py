import pandas as pd
import btbox
import btbox.backtest
import btbox.strategy
import btbox.market


class Algo(btbox.Strategy):
    name = 'Algo'

    def step(self, i, now, broker):
        # this contains the algo logics
        assert 0
        pass


ohlcv = pd.read_csv('tests/SPY.csv', index_col='Date', parse_dates=True)


def test1():
    btbox.create_backtest(Algo, ohlcv).run()


def test2():
    btbox.backtest.create(Algo, ohlcv).run()


def test3():
    bt = btbox.backtest.create(Algo, ohlcv)
    bt.run()


def test4():
    strategy = Algo()
    market = btbox.market.Market(ohlcv)
    backtest = btbox.backtest.Backtest(strategy, market)
    backtest.run()
