from btbox.broker import Broker
from btbox.strategy import Strategy
from btbox.datasource.utils import import_yahoo_csv
from btbox.backtest.utils import create_backtest
from btbox.strategy.decorator import interval


def test_nav_plot(mocker):
    dfs = {'SPY': import_yahoo_csv('tests/_data_/SPY_bar1day.csv')}

    class S1(Strategy):
        name = 'MarkMe'

        @interval(100)
        def step(self, b: Broker):
            b.portfolio.trade_target_weight('SPY', 0.5)

    results = create_backtest([S1, ], dfs, start='2020-01-01').run()
    mocker.patch('btbox.backtest.results.selected.nav.Nav.plot')
    results['MarkMe'].nav.plot()
    results['MarkMe'].nav.plot.assert_called_once()
    mocker.patch('btbox.backtest.results.selected.Selected.plot')
    results['MarkMe'].plot()
    results['MarkMe'].plot.assert_called_once()
