from datetime import datetime
import pandas as pd
import numpy as np
import btbox
import btbox.backtest
from btbox.broker import Broker
from btbox.datasource import DataSource
import logging


logger = logging.getLogger()
logger.setLevel(logging.INFO)


def test_main_loop_on_dummy_data():
    dates = pd.date_range(start='2010-01-01', end='2020-12-31')
    dataframes = {'SPY': pd.DataFrame(
        np.random.randint(0, 1000, size=len(dates)), index=dates)}

    class CustomStrategy(btbox.Strategy):
        name = 'test main loop on dummy data'

        def step(self, i: int, now: datetime, broker: Broker):
            # this contains the algo logics
            if i % 1000 == 0:
                logger.info(dict(i=i, now=now, broker=broker))
                assert now == broker._now == broker._market._now

    btbox.create_backtest(CustomStrategy, dataframes).run()


def test_main_loop():
    dataframes = {'SPY': DataSource.import_yahoo_csv('tests/SPY.csv')}

    class CustomStrategy(btbox.Strategy):
        name = 'test main loop'

        def step(self, i: int, now: datetime, broker: Broker):
            # this contains the algo logics
            if i % 1000 == 0:
                logger.info(dict(i=i, now=now, broker=broker))
                assert now == broker._now == broker._market._now

    btbox.create_backtest(CustomStrategy, dataframes).run()
