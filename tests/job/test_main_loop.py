from pandas import date_range, DataFrame, Series
import numpy as np
import btbox
import btbox.job
from btbox.broker import Broker
from btbox.datasource.utils import import_yahoo_csv
import logging


logger = logging.getLogger()
logger.setLevel(logging.INFO)


def test_main_loop_on_dummy_data():
    dates = Series(date_range(start='2010-01-01',
                   end='2020-12-31'), name='Date')
    columns = ['Open', 'High', 'Low', 'Close', 'Volume']
    dfs = {'SPY': DataFrame(
        np.random.randint(0, 1000, size=(len(dates), 5)),
        columns=columns, index=dates)}

    class CustomStrategy(btbox.Strategy):
        name = 'test main loop on dummy data'

        def step(self, i: int, b: Broker):
            # this contains the algo logics
            if i % 1000 == 0:
                logger.info(dict(i=i, now=b.now, broker=b))
                assert b.now == b._clock.now == b._market._clock.now

    btbox.create_job(CustomStrategy, dfs).run()


def test_main_loop():
    dfs = {'SPY': import_yahoo_csv('tests/_data_/SPY_bar1day.csv')}

    class CustomStrategy(btbox.Strategy):
        name = 'test main loop'

        def step(self, i: int, b: Broker):
            # this contains the algo logics
            if i % 1000 == 0:
                logger.info(dict(i=i, now=b.now, broker=b))
                assert b.now == b._clock.now == b._market._clock.now

    btbox.create_job(CustomStrategy, dfs).run()
