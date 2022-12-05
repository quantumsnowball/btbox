from btbox.strategy import Strategy
from btbox.datasource.utils import import_yahoo_csv
from btbox.backtest.utils import create_backtest


def test_navs_values():
    dfs = {'SPY': import_yahoo_csv('tests/_data_/SPY_bar1day.csv')}

    class S1(Strategy):
        name = 'test-nav 2m'
        capital = 2e6

    class S2(Strategy):
        name = 'test-nav 5m'
        capital = 5e6

    class S3(Strategy):
        name = 'test-nav 8m'
        capital = 8e6

    class S4(Strategy):
        name = 'test-nav 10m'
        capital = 1e7

    results = create_backtest([S1, S2, S3, S4], dfs,
                              start='2020-01-01', window=30).run()
    assert results.navs.values.shape[1] == 4
    assert results.navs.values.iloc[-1].values.tolist() == [2e6, 5e6, 8e6, 1e7]


def test_navs_plot(mocker):
    dfs = {'SPY': import_yahoo_csv('tests/_data_/SPY_bar1day.csv')}

    class S1(Strategy):
        name = 'test-nav 2m'
        capital = 2e6

    results = create_backtest([S1], dfs, start='2020-01-01', window=30).run()
    fn_line = mocker.patch('btbox.backtest.results.navs.px.line')
    results.navs.plot()
    fn_line.assert_called_once()
    fn_line.reset_mock()
    results.plot()
    fn_line.assert_called_once()
