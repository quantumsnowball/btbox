import btbox
import btbox.job
import btbox.job.utils
from btbox.job import Job
from btbox.broker import Broker
from btbox.share import Clock
from btbox.datasource import DataSource
from btbox.datasource.utils import import_yahoo_csv
from btbox.market import Market


class CustomStrategy(btbox.Strategy):
    name = 'Algo'

    def step(self, i: int, b: Broker):
        # this contains the algo logics
        pass


dataframes = {'SPY': import_yahoo_csv('tests/_data_/SPY_bar1day.csv')}


def test1():
    btbox.create_job(CustomStrategy, dataframes).run()


def test2():
    btbox.job.utils.create_job(CustomStrategy, dataframes).run()


def test3():
    bt = btbox.job.utils.create_job(CustomStrategy, dataframes)
    bt.run()


def test4():
    clock = Clock(Job)
    datasource = DataSource(dataframes)
    market = Market(datasource, clock)
    broker = Broker(market, clock)
    strategy = CustomStrategy(broker, clock)
    job = Job(strategy, clock)
    job.run()
