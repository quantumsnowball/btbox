import btbox
import btbox.job
import btbox.job.utils
from btbox.job import Job
from btbox.strategy import Strategy
from btbox.broker import Broker
from btbox.share import Clock
from btbox.datasource import DataSource
from btbox.datasource.utils import import_yahoo_csv
from btbox.market import Market
from btbox.strategy.decorator import interval


class StBasic(Strategy):
    name = 'Basic'

    def step(self, i: int, b: Broker):
        # this contains the algo logics
        pass


class StBenchmarak(Strategy):
    name = 'Benchmark'

    def initial(self, b: Broker):
        pass


class StDecorator(Strategy):
    name = 'Decorator'

    def initial(self, b: Broker):
        pass

    @interval(10)
    def step(self, b: Broker):
        pass


dataframes = {'SPY': import_yahoo_csv('tests/_data_/SPY_bar1day.csv')}


def test1():
    btbox.create_job(StBasic, dataframes).run()
    btbox.create_job(StBenchmarak, dataframes).run()
    btbox.create_job(StDecorator, dataframes).run()


def test2():
    btbox.job.utils.create_job(StBasic, dataframes).run()
    btbox.job.utils.create_job(StBenchmarak, dataframes).run()
    btbox.job.utils.create_job(StDecorator, dataframes).run()


def test3():
    bt = btbox.job.utils.create_job(StBasic, dataframes)
    bt.run()
    bt = btbox.job.utils.create_job(StBenchmarak, dataframes)
    bt.run()
    bt = btbox.job.utils.create_job(StDecorator, dataframes)
    bt.run()


def test4():
    def run_job(St):
        clock = Clock(Job)
        datasource = DataSource(dataframes)
        market = Market(datasource, clock)
        broker = Broker(market, clock)
        strategy = St(broker, clock)
        job = Job(strategy, clock)
        job.run()
    for St in [StBasic, StBenchmarak, StDecorator]:
        run_job(St)
