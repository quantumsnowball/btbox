from pandas import to_datetime
from btbox.broker import Broker
from btbox.job.utils import create_job
from btbox.strategy import Strategy
from btbox.datasource.utils import import_yahoo_csv
import logging


logger = logging.getLogger()
logger.setLevel(logging.INFO)


def test_start_end_window_timeline():
    INI_CASH = 1e6
    SYMBOL = 'SPY'
    START = '2010-01-04'
    END = '2020-12-31'
    WINDOW = 100
    dataframes = {SYMBOL: import_yahoo_csv('tests/_data_/SPY_bar1day.csv')}

    class Benchmark(Strategy):
        name = 'Benchmark'

        def step(self, i: int, broker: Broker):
            if i == 0:
                broker.order.deposit(INI_CASH)
                broker.portfolio.trade_target_weight(SYMBOL, 1.0)
                assert broker.now == to_datetime(START)
            if i % 250 == 0:
                win = broker.market.get_ohlcv_window_at(
                    SYMBOL, broker.now, WINDOW)
                assert len(win) == WINDOW
                assert win.index[-1] <= broker.now

    job = create_job(Benchmark, dataframes,
                     start=START,
                     end=END,
                     window=WINDOW)
    result = job.run()
    assert result is not None
