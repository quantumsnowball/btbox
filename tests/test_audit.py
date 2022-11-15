from datetime import datetime
import pandas as pd
import btbox
import btbox.backtest
from btbox.broker import Broker
import logging


logger = logging.getLogger()
logger.setLevel(logging.INFO)


def test_audit_cash():
    ini_cash = 1_234_567
    dataframe = pd.read_csv('tests/SPY.csv',
                            index_col='Date', parse_dates=True)

    class CustomStrategy(btbox.Strategy):
        name = 'test audit cash'

        def step(self, i: int, now: datetime, broker: Broker):
            # initial deposit
            if i == 0:
                broker.deposit(ini_cash)
            if i % 1000 == 0:
                logger.info(dict(i=i, now=now, cash=broker.cash))
                assert broker.cash == ini_cash

    btbox.create_backtest(CustomStrategy, dataframe).run()
