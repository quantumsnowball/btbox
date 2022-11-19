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
    dfs = {SYMBOL: import_yahoo_csv('tests/_data_/SPY_bar1day.csv')}

    class Benchmark(Strategy):
        name = 'Benchmark'

        def step(self, i: int, b: Broker):
            if i == 0:
                b.order.deposit(INI_CASH)
                b.portfolio.trade_target_weight(SYMBOL, 1.0)

    class CustomStrategy(Strategy):
        name = 'CustomStrategy'

        def step(self, i: int, b: Broker):
            if i == 0:
                b.order.deposit(INI_CASH)
                b.portfolio.trade_target_weight(SYMBOL, 0.5)

    bt = create_backtest([Benchmark, CustomStrategy], dfs)
    results = bt.run()
    assert results is not None
