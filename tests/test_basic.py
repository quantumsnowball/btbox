import btbox
import btbox.backtest
import btbox.backtest.utils
from btbox.backtest import Backtest
from btbox.broker import Broker
from btbox.clock import Clock
from btbox.datasource import DataSource
from btbox.datasource.utils import import_yahoo_csv
from btbox.market import Market


class CustomStrategy(btbox.Strategy):
    name = 'Algo'

    def step(self, i, now, broker):
        # this contains the algo logics
        pass


dataframes = {'SPY': import_yahoo_csv('tests/SPY.csv')}


def test1():
    btbox.create_backtest(CustomStrategy, dataframes).run()


def test2():
    btbox.backtest.utils.create(CustomStrategy, dataframes).run()


def test3():
    bt = btbox.backtest.utils.create(CustomStrategy, dataframes)
    bt.run()


def test4():
    clock = Clock()
    datasource = DataSource(dataframes)
    market = Market(datasource, clock)
    broker = Broker(market, clock)
    strategy = CustomStrategy(broker, clock)
    backtest = Backtest(strategy, clock)
    backtest.run()
