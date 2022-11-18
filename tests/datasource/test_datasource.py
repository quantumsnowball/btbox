from pandas import to_datetime
from btbox.broker import Broker
from btbox.job.utils import create_job
from btbox.strategy import Strategy
from btbox.datasource.utils import import_yahoo_csv
import logging


logger = logging.getLogger()
logger.setLevel(logging.INFO)


def test_all_market_functions():
    INI_CASH = 1e6
    SYMBOL = 'SPY'
    START = '2000-01-04'
    END = '2020-12-31'
    WINDOW = 100
    dfs = {SYMBOL: import_yahoo_csv('tests/_data_/SPY_bar1day.csv')}

    class Benchmark(Strategy):
        name = 'Benchmark'

        def step(self, i: int, b: Broker):
            if i == 0:
                b.order.deposit(INI_CASH)
                b.portfolio.trade_target_weight(SYMBOL, 1.0)
            if i % 63 == 0:
                close = b.market.get_close(SYMBOL)
                ohlcv = b.market.get_ohlcv(SYMBOL)
                assert close == ohlcv.Close == \
                    dfs[SYMBOL].loc[b.now, 'Close']

    job = create_job(Benchmark, dfs,
                     start=START,
                     end=END,
                     window=WINDOW)
    result = job.run()
    assert result is not None


def test_start_end_window_timeline():
    INI_CASH = 1e6
    SYMBOL = 'SPY'
    START = '2010-01-04'
    END = '2020-12-31'
    WINDOW = 100
    dfs = {SYMBOL: import_yahoo_csv('tests/_data_/SPY_bar1day.csv')}

    class Benchmark(Strategy):
        name = 'Benchmark'

        def step(self, i: int, b: Broker):
            if i == 0:
                b.order.deposit(INI_CASH)
                b.portfolio.trade_target_weight(SYMBOL, 1.0)
                assert b.now == to_datetime(START)
            if i % 250 == 0:
                win_close = b.market.get_close_window(SYMBOL)
                assert len(win_close) == WINDOW
                assert win_close.index[-1] <= b.now
                win_ohlcv = b.market.get_ohlcv_window(SYMBOL)
                assert len(win_ohlcv) == WINDOW
                assert win_ohlcv.index[-1] <= b.now

    job = create_job(Benchmark, dfs,
                     start=START,
                     end=END,
                     window=WINDOW)
    result = job.run()
    assert result is not None
