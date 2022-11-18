from pandas import DataFrame
from pandas.io.formats.style import Styler
from btbox.backtest.utils import create_backtest
from btbox.broker import Broker
from btbox.strategy import Strategy
from btbox.datasource.utils import import_yahoo_csv
import logging


logger = logging.getLogger()
logger.setLevel(logging.INFO)


def test_dashboard():
    INI_CASH = 1e6
    SYMBOL = 'SPY'
    dataframes = {SYMBOL: import_yahoo_csv('tests/_data_/SPY_bar1day.csv')}

    class Benchmark(Strategy):
        name = 'Benchmark'

        def step(self, i: int, broker: Broker):
            if i == 0:
                broker.order.deposit(INI_CASH)
                broker.portfolio.trade_target_weight(SYMBOL, 1.0)

    class CustomStrategy(Strategy):
        name = 'CustomStrategy'

        def step(self, i: int, broker: Broker):
            if i == 0:
                broker.order.deposit(INI_CASH)
                broker.portfolio.trade_target_weight(SYMBOL, 0.5)

    bt = create_backtest([Benchmark, CustomStrategy], dataframes)
    results = bt.run()
    dashboard = results.dashboard()
    assert isinstance(dashboard, DataFrame)
    assert dashboard.shape == (2, 8)
    dashboard_pretty = results.dashboard_pretty()
    assert isinstance(dashboard_pretty, Styler)
    assert dashboard_pretty.data.shape == (2, 8)
