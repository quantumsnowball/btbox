from datetime import datetime
import pandas as pd
import btbox
import btbox.backtest
from btbox.broker import Broker
import logging


logger = logging.getLogger()
logger.setLevel(logging.INFO)


dataframe = pd.read_csv('tests/SPY.csv', index_col='Date', parse_dates=True)


def test_main_loop():
    class CustomStrategy(btbox.Strategy):
        name = 'Algo'

        def step(self, i: int, now: datetime, broker: Broker):
            # this contains the algo logics
            if i % 1000 == 0:
                logger.info(dict(i=i, now=now, broker=broker))
                assert now == broker._now == broker._market._now

    btbox.create_backtest(CustomStrategy, dataframe).run()
