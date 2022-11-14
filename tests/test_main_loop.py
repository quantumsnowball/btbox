from datetime import datetime
import pandas as pd
import numpy as np
import btbox
import btbox.backtest
from btbox.broker import Broker
import logging


logger = logging.getLogger()
logger.setLevel(logging.INFO)


def test_main_loop_on_dummy_data():
    dates = pd.date_range(start='2010-01-01', end='2020-12-31')
    dataframe = pd.DataFrame(np.random.randint(
        0, 1000, size=len(dates)), index=dates)

    class CustomStrategy(btbox.Strategy):
        name = 'test main loop on dummy data'

        def step(self, i: int, now: datetime, broker: Broker):
            # this contains the algo logics
            if i % 1000 == 0:
                logger.info(dict(i=i, now=now, broker=broker))
                assert now == broker._now == broker._market._now

    btbox.create_backtest(CustomStrategy, dataframe).run()


def test_main_loop():
    dataframe = pd.read_csv('tests/SPY.csv',
                            index_col='Date', parse_dates=True)

    class CustomStrategy(btbox.Strategy):
        name = 'test main loop'

        def step(self, i: int, now: datetime, broker: Broker):
            # this contains the algo logics
            if i % 1000 == 0:
                logger.info(dict(i=i, now=now, broker=broker))
                assert now == broker._now == broker._market._now

    btbox.create_backtest(CustomStrategy, dataframe).run()
