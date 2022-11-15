from datetime import datetime
import btbox
import btbox.backtest
from btbox.broker import Broker
from btbox.datasource import DataSource
import logging


logger = logging.getLogger()
logger.setLevel(logging.INFO)


def test_audit_cash():
    ini_cash = 1_234_567
    dataframes = {'SPY': DataSource.import_yahoo_csv('tests/SPY.csv')}

    class CustomStrategy(btbox.Strategy):
        name = 'test audit cash'

        def step(self, i: int, now: datetime, broker: Broker):
            # initial deposit
            if i == 0:
                broker.deposit(ini_cash)
            if i % 1000 == 0:
                logger.info(dict(i=i, now=now, cash=broker.cash))
                assert broker.cash == ini_cash

    btbox.create_backtest(CustomStrategy, dataframes).run()


def test_record_cash():
    ini_cash = 1_234_567
    dataframes = {'SPY': DataSource.import_yahoo_csv('tests/SPY.csv')}

    class CustomStrategy(btbox.Strategy):
        name = 'test record cash'

        def step(self, i: int, now: datetime, broker: Broker):
            # initial deposit
            if i == 0:
                broker.deposit(ini_cash)
            if i % 1000 == 0 and i > 0:
                logger.info(dict(i=i, now=now, cash=broker.cash))
                assert broker.report.nav_history.iloc[-1] == ini_cash

    btbox.create_backtest(CustomStrategy, dataframes).run()


def test_buy_stock():
    INI_CASH = 1e6
    SYMBOL = 'SPY'
    QUANTITY = 10
    dataframes = {SYMBOL: DataSource.import_yahoo_csv('tests/SPY.csv')}

    class CustomStrategy(btbox.Strategy):
        name = 'test buy stock'

        def step(self, i: int, now: datetime, broker: Broker):
            # initial deposit
            if i == 0:
                broker.deposit(INI_CASH)
                broker.trade(SYMBOL, +QUANTITY)
                broker.withdrawal(broker.cash)
                assert broker.cash == 0
            if i % 1000 == 0 and i > 0:
                logger.info(dict(i=i, now=now, SPY=broker.positions[SYMBOL]))
                assert broker.positions[SYMBOL] == QUANTITY
                assert broker.market.get_close_at(SYMBOL, now) * QUANTITY == \
                    broker.audit.nav_account()

    btbox.create_backtest(CustomStrategy, dataframes).run()
