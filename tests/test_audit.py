from datetime import datetime
from btbox import create_backtest
from btbox.broker import Broker
from btbox.strategy import Strategy
from btbox.datasource.utils import import_yahoo_csv
import logging


logger = logging.getLogger()
logger.setLevel(logging.INFO)


def test_audit_cash():
    INI_CASH = 1_234_567
    dataframes = {'SPY': import_yahoo_csv('tests/SPY.csv')}

    class CustomStrategy(Strategy):
        name = 'test audit cash'

        def step(self, i: int, now: datetime, broker: Broker):
            # initial deposit
            if i == 0:
                broker.order.deposit(INI_CASH)
            if i % 1000 == 0:
                logger.info(dict(i=i, now=now, cash=broker.cash))
                assert broker.cash == INI_CASH

    create_backtest(CustomStrategy, dataframes).run()


def test_record_cash():
    INI_CASH = 1_234_567
    dataframes = {'SPY': import_yahoo_csv('tests/SPY.csv')}

    class CustomStrategy(Strategy):
        name = 'test record cash'

        def step(self, i: int, now: datetime, broker: Broker):
            # initial deposit
            if i == 0:
                broker.order.deposit(INI_CASH)
            if i % 1000 == 0 and i > 0:
                logger.info(dict(i=i, now=now, cash=broker.cash))
                assert broker.report.nav.iloc[-1] == INI_CASH

    create_backtest(CustomStrategy, dataframes).run()


def test_buy_stock():
    INI_CASH = 1e6
    SYMBOL = 'SPY'
    QUANTITY = 10
    dataframes = {SYMBOL: import_yahoo_csv('tests/SPY.csv')}

    class CustomStrategy(Strategy):
        name = 'test buy stock'

        def step(self, i: int, now: datetime, broker: Broker):
            # initial deposit
            if i == 0:
                broker.order.deposit(INI_CASH)
                broker.order.trade(SYMBOL, +QUANTITY)
                broker.order.withdrawal(broker.cash)
                assert broker.cash == 0
            if i % 1000 == 0 and i > 0:
                logger.info(dict(i=i, now=now, SPY=broker.positions[SYMBOL]))
                assert broker.positions[SYMBOL] == QUANTITY
                assert broker.market.get_close_at(SYMBOL, now) * QUANTITY == \
                    broker.audit.nav_account()

    create_backtest(CustomStrategy, dataframes).run()


def test_nav_report():
    INI_CASH = 1e6
    SYMBOL = 'SPY'
    QUANTITY = 10
    dataframes = {SYMBOL: import_yahoo_csv('tests/SPY.csv')}

    class CustomStrategy(Strategy):
        name = 'test nav report'

        def step(self, i: int, now: datetime, broker: Broker):
            # initial deposit
            if i == 0:
                broker.order.deposit(INI_CASH)
            if i % 1000 == 0:
                broker.order.trade(SYMBOL, +QUANTITY)
                logger.info(dict(i=i, now=now, SPY=broker.positions[SYMBOL]))
                assert broker.report.trades.iloc[-1].Symbol == 'SPY'
                assert broker.report.trades.Quantity.sum() == \
                    (i // 1000 + 1) * QUANTITY

    create_backtest(CustomStrategy, dataframes).run()
