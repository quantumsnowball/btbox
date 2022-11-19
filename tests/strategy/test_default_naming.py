from btbox.broker import Broker
from btbox.strategy import Strategy
from btbox.datasource.utils import import_yahoo_csv
from btbox.backtest.utils import create_backtest


def test_default_naming():
    dfs = {'SPY': import_yahoo_csv('tests/_data_/SPY_bar1day.csv')}

    class S1(Strategy):
        name = 'CustomName'

        def initial(self, b: Broker):
            b.portfolio.trade_target_weight('SPY', 1.0)

    class S2(Strategy):
        def initial(self, b: Broker):
            b.portfolio.trade_target_weight('SPY', 1.0)

    results = create_backtest([S1, S2], dfs, start='2020-01-01').run()
    assert results.dashboard().index.tolist() == ['CustomName', 'S2']
