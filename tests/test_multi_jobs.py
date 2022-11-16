from datetime import datetime
from btbox.backtest.utils import create_backtest
from btbox.broker import Broker
from btbox.strategy import Strategy
from btbox.datasource.utils import import_yahoo_csv
import logging


logger = logging.getLogger()
logger.setLevel(logging.INFO)


def test_multi_jobs_basic():
    INI_CASH = 1e6
    SYMBOL = 'SPY'
    dataframes = {SYMBOL: import_yahoo_csv('tests/SPY.csv')}

    class Benchmark(Strategy):
        name = 'Benchmark'

        def step(self, i: int, now: datetime, broker: Broker):
            if i == 0:
                broker.order.deposit(INI_CASH)
                broker.portfolio.trade_target_weight(SYMBOL, 1.0)

    class CustomStrategy(Strategy):
        name = 'CustomStrategy'

        def step(self, i: int, now: datetime, broker: Broker):
            if i == 0:
                broker.order.deposit(INI_CASH)
                broker.portfolio.trade_target_weight(SYMBOL, 0.5)

    bt = create_backtest([Benchmark, CustomStrategy], dataframes)
    bt.run()
