import pandas as pd
import btbox
import btbox.backtest
from btbox.backtest import Backtest
from btbox.broker import Broker
from btbox.datasource import DataSource
from btbox.market import Market


class CustomStrategy(btbox.Strategy):
    name = 'Algo'

    def step(self, i, now, broker):
        # this contains the algo logics
        pass


dataframe = pd.read_csv('tests/SPY.csv', index_col='Date', parse_dates=True)


def test1():
    btbox.create_backtest(CustomStrategy, dataframe).run()


def test2():
    btbox.backtest.create(CustomStrategy, dataframe).run()


def test3():
    bt = btbox.backtest.create(CustomStrategy, dataframe)
    bt.run()


def test4():
    datasource = DataSource(dataframe)
    market = Market(datasource)
    broker = Broker(market)
    strategy = CustomStrategy(broker)
    backtest = Backtest(strategy)
    backtest.run()
