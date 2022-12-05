from pandas import DataFrame, to_datetime
import btbox
from btbox.broker import Broker
from btbox.datasource.simulation import make_random_ohlcv
from btbox.strategy import Strategy
from btbox.strategy.decorator import interval


class StDummy(Strategy):
    @interval(1)
    def step(self, b: Broker):
        pass


def test_make_random_ohlcv():
    SYMBOL = 'DUMMY'
    START = to_datetime('2020-01-01')
    END = to_datetime('2021-12-31')

    df = make_random_ohlcv(START, END,
                           p0=100,
                           mu=0.1, sigma=0.2)
    assert isinstance(df, DataFrame)
    assert df.shape[1] == 5

    dfs = {SYMBOL: df}
    btbox.create_job(StDummy, dfs).run()
