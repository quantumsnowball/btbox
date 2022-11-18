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
    dataframes = {'SPY': import_yahoo_csv('tests/_data_/SPY_bar1day.csv')}

    class S1(Strategy):
        name = 'test audit cash'
        capital = 0

        def step(self, i: int, b: Broker):
            if i == 0:
                b.order.deposit(INI_CASH)
            if i % 1000 == 0:
                logger.info(dict(i=i, now=b.now, cash=b.cash))
                assert b.cash == INI_CASH

    s1_nav = create_job(S1, dataframes).run().report.nav[-1]

    class S2(Strategy):
        name = 'test deposit in initial'
        capital = 0

        def initial(self, b: Broker):
            b.order.deposit(INI_CASH)

        @interval(1000)
        def step(self, b: Broker):
            logger.info(dict(now=b.now, cash=b.cash))
            assert b.cash == INI_CASH

    s2_nav = create_job(S2, dataframes).run().report.nav[-1]

    class S3(Strategy):
        name = 'test default capital'
        capital = INI_CASH

        @interval(1000)
        def step(self, b: Broker):
            logger.info(dict(now=b.now, cash=b.cash))
            assert b.cash == INI_CASH

    s3_nav = create_job(S3, dataframes).run().report.nav[-1]

    assert s1_nav == s2_nav == s3_nav


def test_record_cash():
    INI_CASH = 1_234_567
    dataframes = {'SPY': import_yahoo_csv('tests/_data_/SPY_bar1day.csv')}

    class S1(Strategy):
        name = 'test record cash'
        capital = 0

        def step(self, i: int, b: Broker):
            if i == 0:
                b.order.deposit(INI_CASH)
            if i % 1000 == 0 and i > 0:
                logger.info(dict(i=i, now=b.now, cash=b.cash))
                assert b.report.nav.iloc[-1] == INI_CASH

    s1_nav = create_job(S1, dataframes).run().report.nav[-1]

    class S2(Strategy):
        name = 'test record cash using decorator'
        capital = INI_CASH

        @interval(1000, initial=False)
        def step(self, b: Broker):
            logger.info(dict(now=b.now, cash=b.cash))
            assert b.report.nav.iloc[-1] == INI_CASH

    s2_nav = create_job(S2, dataframes).run().report.nav[-1]

    assert s1_nav == s2_nav


def test_buy_stock():
    SYMBOL = 'SPY'
    QUANTITY = 10
    dataframes = {SYMBOL: import_yahoo_csv('tests/_data_/SPY_bar1day.csv')}

    class S1(Strategy):
        name = 'test buy stock'

        def step(self, i: int, b: Broker):
            if i == 0:
                assert b.cash == 1e6
                b.order.trade(SYMBOL, +QUANTITY)
                b.order.withdrawal(b.cash)
                assert b.cash == 0
            if i % 1000 == 0 and i > 0:
                logger.info(dict(i=i, now=b.now, SPY=b.positions[SYMBOL]))
                assert b.positions[SYMBOL] == QUANTITY
                assert b.market.get_close(SYMBOL) * QUANTITY == \
                    b.audit.nav_account()

    s1_nav = create_job(S1, dataframes).run().report.nav[-1]

    class S2(Strategy):
        name = 'test buy stock with decorator'

        def initial(self, b: Broker):
            assert b.cash == 1e6
            b.order.trade(SYMBOL, +QUANTITY)
            b.order.withdrawal(b.cash)
            assert b.cash == 0

        @interval(1000, initial=False)
        def step(self, b: Broker):
            logger.info(dict(now=b.now, SPY=b.positions[SYMBOL]))
            assert b.positions[SYMBOL] == QUANTITY
            assert b.market.get_close(SYMBOL) * QUANTITY == \
                b.audit.nav_account()

    s2_nav = create_job(S2, dataframes).run().report.nav[-1]

    assert s1_nav == s2_nav


def test_nav_report():
    SYMBOL = 'SPY'
    QUANTITY = 10
    dataframes = {SYMBOL: import_yahoo_csv('tests/_data_/SPY_bar1day.csv')}

    class CustomStrategy(Strategy):
        name = 'test nav report'

        def step(self, i: int, b: Broker):
            if i == 0:
                assert b.cash == 1e6
            if i % 1000 == 0:
                b.order.trade(SYMBOL, +QUANTITY)
                logger.info(dict(i=i, now=b.now, SPY=b.positions[SYMBOL]))
                assert b.report.trades.iloc[-1].Symbol == 'SPY'
                assert b.report.trades.Quantity.sum() == \
                    (i // 1000 + 1) * QUANTITY

    create_job(CustomStrategy, dataframes).run()
