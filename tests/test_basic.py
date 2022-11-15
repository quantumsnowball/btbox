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


dataframes = {'SPY': DataSource.import_yahoo_csv('tests/SPY.csv')}


def test1():
    btbox.create_backtest(CustomStrategy, dataframes).run()


def test2():
    btbox.backtest.create(CustomStrategy, dataframes).run()


def test3():
    bt = btbox.backtest.create(CustomStrategy, dataframes)
    bt.run()


def test4():
    datasource = DataSource(dataframes)
    market = Market(datasource)
    broker = Broker(market)
    strategy = CustomStrategy(broker)
    backtest = Backtest(strategy)
    backtest.run()
