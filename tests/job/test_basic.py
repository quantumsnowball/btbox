import btbox
import btbox.job
import btbox.job.utils
from btbox.job import Job
from btbox.broker import Broker
from btbox.share import Clock
from btbox.datasource import DataSource
from btbox.datasource.utils import import_yahoo_csv
from btbox.market import Market
from tests.helper import basicFullInterval10, basicInitialOnly, basicStepOnly


StBasic = basicStepOnly('Basic')
StBenchmarak = basicInitialOnly('Benchmark')
StDecorator = basicFullInterval10('Decorator')


dfs = {'SPY': import_yahoo_csv('tests/_data_/SPY_bar1day.csv')}


def test1():
    btbox.create_job(StBasic, dfs).run()
    btbox.create_job(StBenchmarak, dfs).run()
    btbox.create_job(StDecorator, dfs).run()


def test2():
    btbox.job.utils.create_job(StBasic, dfs).run()
    btbox.job.utils.create_job(StBenchmarak, dfs).run()
    btbox.job.utils.create_job(StDecorator, dfs).run()


def test3():
    bt = btbox.job.utils.create_job(StBasic, dfs)
    bt.run()
    bt = btbox.job.utils.create_job(StBenchmarak, dfs)
    bt.run()
    bt = btbox.job.utils.create_job(StDecorator, dfs)
    bt.run()


def test4():
    def run_job(St):
        clock = Clock(Job)
        datasource = DataSource(dfs)
        market = Market(datasource, clock)
        broker = Broker(market, clock)
        strategy = St(broker, clock)
        job = Job(strategy, clock)
        job.run()
    for St in [StBasic, StBenchmarak, StDecorator]:
        run_job(St)
