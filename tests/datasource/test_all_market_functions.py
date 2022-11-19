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
