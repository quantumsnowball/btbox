from btbox import create_job
from btbox.broker import Broker
from btbox.strategy import Strategy
from btbox.strategy.decorator import interval
from btbox.datasource.utils import import_yahoo_csv
import logging


logger = logging.getLogger()
logger.setLevel(logging.INFO)


def test_audit_cash():
    INI_CASH = 1_234_567
    dfs = {'SPY': import_yahoo_csv('tests/_data_/SPY_bar1day.csv')}

    class S1(Strategy):
        name = 'test audit cash'
        capital = 0

        def step(self, i: int, b: Broker):
            if i == 0:
                b.order.deposit(INI_CASH)
            if i % 1000 == 0:
                logger.info(dict(i=i, now=b.now, cash=b.cash))
                assert b.cash == INI_CASH

    s1_nav = create_job(S1, dfs).run().report.nav[-1]

    class S2(Strategy):
        name = 'test deposit in initial'
        capital = 0

        def initial(self, b: Broker):
            b.order.deposit(INI_CASH)

        @interval(1000)
        def step(self, b: Broker):
            logger.info(dict(now=b.now, cash=b.cash))
            assert b.cash == INI_CASH

    s2_nav = create_job(S2, dfs).run().report.nav[-1]

    class S3(Strategy):
        name = 'test default capital'
        capital = INI_CASH

        @interval(1000)
        def step(self, b: Broker):
            logger.info(dict(now=b.now, cash=b.cash))
            assert b.cash == INI_CASH

    s3_nav = create_job(S3, dfs).run().report.nav[-1]

    assert s1_nav == s2_nav == s3_nav
