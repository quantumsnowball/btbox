from btbox.broker import Broker
from btbox.strategy import Strategy
from btbox.datasource.utils import import_yahoo_csv
from btbox.backtest.utils import create_backtest
from btbox.strategy.decorator import interval


def test_bfill_ffill():
    dfs = {'SPY': import_yahoo_csv('tests/_data_/SPY_bar1day.csv')}

    class S1(Strategy):
        name = 'Line'

        @interval(1000)
        def step(self, b: Broker):
            self.journal.mark(8888, 'line-8888')
            self.journal.mark(9999, 'line-9999')

    results = create_backtest(
        [S1, ], dfs, start='2020-01-01', window=30).run()
    df_pre = results['Line'].journals['line-8888'].values
    df_bfill = results['Line'].journals['line-8888'].bfill.values
    assert df_bfill.equals(df_pre.bfill())
    df_pre = results['Line'].journals['line-9999'].values
    df_ffill = results['Line'].journals['line-9999'].ffill.values
    assert df_ffill.equals(df_pre.ffill())


def test_plot_line(mocker):
    dfs = {'SPY': import_yahoo_csv('tests/_data_/SPY_bar1day.csv')}

    class S1(Strategy):
        name = 'Line'

        @interval(1)
        def step(self, b: Broker):
            self.journal.mark(8888, 'line-8888')
            self.journal.mark(9999, 'line-9999')

    results = create_backtest(
        [S1, ], dfs, start='2020-01-01', window=30).run()
    result = results['Line']
    fn_Figure = mocker.patch(
        'btbox.backtest.results.selected.utils.Figure')
    fn_Scatter = mocker.patch(
        'btbox.backtest.results.selected.utils.Scatter')
    result.journals['line-8888', 'line-9999'].plot_line()
    fn_Figure.assert_called_once()
    fn_Scatter.assert_called()


def test_plot_scatter(mocker):
    dfs = {'SPY': import_yahoo_csv('tests/_data_/SPY_bar1day.csv')}

    class S1(Strategy):
        name = 'Scatter'

        def step(self, i: int, b: Broker):
            if i % 2 == 0 and i > 0:
                self.journal.mark(2, 'Every 2 Days')
            if i % 4 == 0 and i > 0:
                self.journal.mark(4, 'Every 4 Days')
            if i % 5 == 0 and i > 0:
                self.journal.mark(4, 'Every 5 Days')

    results = create_backtest(
        [S1, ], dfs, start='2020-01-01', window=30).run()
    result = results['Scatter']
    assert result.journals['Every 2 Days', 'Every 5 Days'].values.shape[1] == 2
    assert result.journals['Every 2 Days', 'Every 4 Days'].values.shape[1] == 2
    fn_Figure = mocker.patch(
        'btbox.backtest.results.selected.utils.Figure')
    fn_Scatter = mocker.patch(
        'btbox.backtest.results.selected.utils.Scatter')
    result.journals['Every 2 Days', 'Every 5 Days'].plot_scatter()
    fn_Figure.assert_called_once()
    fn_Scatter.assert_called()


def test_plot_scatter_on_nav(mocker):
    dfs = {'SPY': import_yahoo_csv('tests/_data_/SPY_bar1day.csv')}

    class S1(Strategy):
        name = 'Nav-Scatter'

        def step(self, i: int, b: Broker):
            if i % 2 == 0 and i > 0:
                self.journal.mark(2, 'Every 2 Days')
            if i % 4 == 0 and i > 0:
                self.journal.mark(4, 'Every 4 Days')
            if i % 5 == 0 and i > 0:
                self.journal.mark(4, 'Every 5 Days')

    results = create_backtest(
        [S1, ], dfs, start='2020-01-01', window=30).run()
    result = results['Nav-Scatter']
    fn_Figure = mocker.patch(
        'btbox.backtest.results.selected.utils.Figure')
    fn_Scatter = mocker.patch(
        'btbox.backtest.results.selected.utils.Scatter')
    result.journals['Every 2 Days', 'Every 5 Days'].plot_scatter_on_nav()
    fn_Figure.assert_called_once()
    fn_Scatter.assert_called()


def test_plot_scatter_on_price(mocker):
    dfs = {'SPY': import_yahoo_csv('tests/_data_/SPY_bar1day.csv')}

    class S1(Strategy):
        name = 'Nav-Scatter'

        def step(self, i: int, b: Broker):
            if i % 2 == 0 and i > 0:
                self.journal.mark(2, 'Every 2 Days')
            if i % 4 == 0 and i > 0:
                self.journal.mark(4, 'Every 4 Days')
            if i % 5 == 0 and i > 0:
                self.journal.mark(4, 'Every 5 Days')

    results = create_backtest(
        [S1, ], dfs, start='2020-01-01', window=30).run()
    result = results['Nav-Scatter']
    fn_Figure = mocker.patch(
        'btbox.backtest.results.selected.utils.Figure')
    fn_Scatter = mocker.patch(
        'btbox.backtest.results.selected.utils.Scatter')
    result.journals['Every 2 Days',
                    'Every 5 Days'].plot_scatter_on_price('SPY')
    fn_Figure.assert_called_once()
    fn_Scatter.assert_called()


def test_plot_line_under_nav(mocker):
    dfs = {'SPY': import_yahoo_csv('tests/_data_/SPY_bar1day.csv')}

    class S1(Strategy):
        name = 'Nav-Line'

        @interval(1)
        def step(self, b: Broker):
            self.journal.mark(8888, 'line-8888')
            self.journal.mark(9999, 'line-9999')

    results = create_backtest(
        [S1, ], dfs, start='2020-01-01', window=30).run()
    result = results['Nav-Line']
    fn_make_subplots = mocker.patch(
        'btbox.backtest.results.selected.utils.make_subplots')
    fn_Scatter = mocker.patch(
        'btbox.backtest.results.selected.utils.Scatter')
    result.journals['line-8888', 'line-9999'].plot_line_under_nav()
    fn_make_subplots.assert_called_once()
    fn_Scatter.assert_called()


def test_plot_line_under_price(mocker):
    dfs = {'SPY': import_yahoo_csv('tests/_data_/SPY_bar1day.csv')}

    class S1(Strategy):
        name = 'Price-Line'

        @interval(1)
        def step(self, b: Broker):
            self.journal.mark(8888, 'line-8888')
            self.journal.mark(9999, 'line-9999')

    results = create_backtest(
        [S1, ], dfs, start='2020-01-01', window=30).run()
    result = results['Price-Line']
    fn_make_subplots = mocker.patch(
        'btbox.backtest.results.selected.utils.make_subplots')
    fn_Scatter = mocker.patch(
        'btbox.backtest.results.selected.utils.Scatter')
    result.journals['line-8888', 'line-9999'].plot_line_under_price('SPY')
    fn_make_subplots.assert_called_once()
    fn_Scatter.assert_called()


def test_plot_scatter_under_nav(mocker):
    dfs = {'SPY': import_yahoo_csv('tests/_data_/SPY_bar1day.csv')}

    class S1(Strategy):
        name = 'Nav-Scatter'

        def step(self, i: int, b: Broker):
            if i % 2 == 0 and i > 0:
                self.journal.mark(2, 'Every 2 Days')
            if i % 4 == 0 and i > 0:
                self.journal.mark(4, 'Every 4 Days')
            if i % 5 == 0 and i > 0:
                self.journal.mark(4, 'Every 5 Days')

    results = create_backtest(
        [S1, ], dfs, start='2020-01-01', window=30).run()
    result = results['Nav-Scatter']
    fn_make_subplots = mocker.patch(
        'btbox.backtest.results.selected.journals.make_subplots')
    fn_Scatter = mocker.patch(
        'btbox.backtest.results.selected.journals.Scatter')
    result.journals['Every 2 Days', 'Every 5 Days'].plot_scatter_under_nav()
    fn_make_subplots.assert_called_once()
    fn_Scatter.assert_called()
