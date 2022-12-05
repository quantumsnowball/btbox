import pytest
import numpy as np
from pandas import DataFrame, to_datetime
import btbox
from btbox.broker import Broker
from btbox.datasource.simulation import make_random_ohlcv
from btbox.strategy import Strategy
from btbox.strategy.decorator import interval


np.random.seed(99999)


def test_make_random_ohlcv():
    START = to_datetime('2020-01-01')
    END = '2021-12-31'
    dfs = [
        make_random_ohlcv(START, END),
        make_random_ohlcv(START, END, '1h'),
        make_random_ohlcv(START, END, '1d', p0=10),
        make_random_ohlcv(START, END, '1d', p0=10, mu=0.5),
        make_random_ohlcv(START, END, '1d', p0=10, sigma=0.5),
        make_random_ohlcv(START, END, '1d', p0=10, max_vol_per_period=20000),
    ]
    for df in dfs:
        assert isinstance(df, DataFrame)
        assert df.shape[1] == 5


@pytest.mark.parametrize('mu,sigma', [
    (.00, .2),
    (.05, .3),
    (.10, .5),
    (.20, .8),
    (.20, .12),
    (.20, .15),
])
def test_dummy_backtest(mu, sigma):
    SYMBOL = 'DUMMY'
    START = to_datetime('2020-01-01')
    END = '2021-12-31'

    df = make_random_ohlcv(START, END, mu=mu, sigma=sigma)
    assert isinstance(df, DataFrame)
    assert df.shape[1] == 5

    class StDummy(Strategy):
        def initial(self, b: Broker) -> None:
            b.portfolio.trade_target_weight(SYMBOL, 1.0)

        @interval(1)
        def step(self, b: Broker):
            pass

    result = btbox.create_job(StDummy, {SYMBOL: df}).run()
    assert sigma / 1.10 < result.metrics.mu_sigma[1] < sigma * 1.10
