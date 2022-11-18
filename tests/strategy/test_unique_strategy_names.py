import pytest
from btbox.broker import Broker
from btbox.strategy import Strategy
from btbox.datasource.utils import import_yahoo_csv
from btbox.backtest.utils import create_backtest


def test_unique_strategy_names():
    dfs = {'SPY': import_yahoo_csv('tests/_data_/SPY_bar1day.csv')}

    class S1(Strategy):
        name = 'SameName'

        def initial(self, b: Broker):
            b.portfolio.trade_target_weight('SPY', 1.0)

    class S2(Strategy):
        name = 'SameName'

        def initial(self, b: Broker):
            b.portfolio.trade_target_weight('SPY', 1.0)

    with pytest.raises(AssertionError):
        create_backtest([S1, S2], dfs, start='2020-01-01').run()
