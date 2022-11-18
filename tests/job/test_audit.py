from btbox import create_job
from btbox.broker import Broker
from btbox.strategy import Strategy
from btbox.datasource.utils import import_yahoo_csv
import logging


logger = logging.getLogger()
logger.setLevel(logging.INFO)


def test_audit_cash():
    INI_CASH = 1_234_567
    dataframes = {'SPY': import_yahoo_csv('tests/_data_/SPY_bar1day.csv')}

    class CustomStrategy(Strategy):
        name = 'test audit cash'

        def step(self, i: int, b: Broker):
            # initial deposit
            if i == 0:
                b.order.deposit(INI_CASH)
            if i % 1000 == 0:
                logger.info(dict(i=i, now=b.now, cash=b.cash))
                assert b.cash == INI_CASH

    create_job(CustomStrategy, dataframes).run()


def test_record_cash():
    INI_CASH = 1_234_567
    dataframes = {'SPY': import_yahoo_csv('tests/_data_/SPY_bar1day.csv')}

    class CustomStrategy(Strategy):
        name = 'test record cash'

        def step(self, i: int, b: Broker):
            # initial deposit
            if i == 0:
                b.order.deposit(INI_CASH)
            if i % 1000 == 0 and i > 0:
                logger.info(dict(i=i, now=b.now, cash=b.cash))
                assert b.report.nav.iloc[-1] == INI_CASH

    create_job(CustomStrategy, dataframes).run()


def test_buy_stock():
    INI_CASH = 1e6
    SYMBOL = 'SPY'
    QUANTITY = 10
    dataframes = {SYMBOL: import_yahoo_csv('tests/_data_/SPY_bar1day.csv')}

    class CustomStrategy(Strategy):
        name = 'test buy stock'

        def step(self, i: int, b: Broker):
            # initial deposit
            if i == 0:
                b.order.deposit(INI_CASH)
                b.order.trade(SYMBOL, +QUANTITY)
                b.order.withdrawal(b.cash)
                assert b.cash == 0
            if i % 1000 == 0 and i > 0:
                logger.info(dict(i=i, now=b.now, SPY=b.positions[SYMBOL]))
                assert b.positions[SYMBOL] == QUANTITY
                assert b.market.get_close_at(SYMBOL, b.now) * QUANTITY == \
                    b.audit.nav_account()

    create_job(CustomStrategy, dataframes).run()


def test_nav_report():
    INI_CASH = 1e6
    SYMBOL = 'SPY'
    QUANTITY = 10
    dataframes = {SYMBOL: import_yahoo_csv('tests/_data_/SPY_bar1day.csv')}

    class CustomStrategy(Strategy):
        name = 'test nav report'

        def step(self, i: int, b: Broker):
            # initial deposit
            if i == 0:
                b.order.deposit(INI_CASH)
            if i % 1000 == 0:
                b.order.trade(SYMBOL, +QUANTITY)
                logger.info(dict(i=i, now=b.now, SPY=b.positions[SYMBOL]))
                assert b.report.trades.iloc[-1].Symbol == 'SPY'
                assert b.report.trades.Quantity.sum() == \
                    (i // 1000 + 1) * QUANTITY

    create_job(CustomStrategy, dataframes).run()
