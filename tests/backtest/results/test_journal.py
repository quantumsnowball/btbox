from btbox.broker import Broker
from btbox.strategy import Strategy
from btbox.datasource.utils import import_yahoo_csv
from btbox.backtest.utils import create_backtest
from btbox.strategy.decorator import interval


dfs = {'SPY': import_yahoo_csv('tests/_data_/SPY_bar1day.csv')}


class ST(Strategy):
    def step(self, i: int, b: Broker):
        # continuous line
        self.journal.mark(8888, 'line-8888')
        self.journal.mark(9999, 'line-9999')
        # individual signal
        if i % 2 == 0 and i > 0:
            self.journal.mark(2, 'every-2d')
        if i % 4 == 0 and i > 0:
            self.journal.mark(4, 'every-4d')
        if i % 5 == 0 and i > 0:
            self.journal.mark(4, 'every-5d')
        # sparse points
        if i % 1000 == 0:
            self.journal.mark(1111, 'point-1111')
            self.journal.mark(2222, 'point-2222')


def test_bfill_ffill():
    result = create_backtest([ST, ], dfs,
                             start='2020-01-01', window=30).run()['ST']
    df_pre = result.journals['point-1111'].values
    df_bfill = result.journals['point-1111'].bfill.values
    assert df_bfill.equals(df_pre.bfill())
    df_pre = result.journals['point-2222'].values
    df_ffill = result.journals['point-2222'].ffill.values
    assert df_ffill.equals(df_pre.ffill())


def test_plot_line(mocker):
    result = create_backtest([ST, ], dfs,
                             start='2020-01-01', window=30).run()['ST']
    fn_Figure = mocker.patch(
        'btbox.backtest.results.selected.utils.Figure')
    fn_Scatter = mocker.patch(
        'btbox.backtest.results.selected.utils.Scatter')
    result.journals['line-8888', 'line-9999'].plot_line()
    fn_Figure.assert_called_once()
    fn_Scatter.assert_called()


def test_plot_scatter(mocker):
    result = create_backtest([ST, ], dfs,
                             start='2020-01-01', window=30).run()['ST']
    assert result.journals['every-2d', 'every-5d'].values.shape[1] == 2
    assert result.journals['every-2d', 'every-4d'].values.shape[1] == 2
    fn_Figure = mocker.patch(
        'btbox.backtest.results.selected.utils.Figure')
    fn_Scatter = mocker.patch(
        'btbox.backtest.results.selected.utils.Scatter')
    result.journals['every-2d', 'every-5d'].plot_scatter()
    fn_Figure.assert_called_once()
    fn_Scatter.assert_called()


def test_plot_line_on_price(mocker):
    result = create_backtest([ST, ], dfs,
                             start='2020-01-01', window=30).run()['ST']
    fn_Figure = mocker.patch(
        'btbox.backtest.results.selected.utils.Figure')
    fn_Scatter = mocker.patch(
        'btbox.backtest.results.selected.utils.Scatter')
    result.journals['line-8888', 'line-9999'].plot_line_on_price('SPY')
    fn_Figure.assert_called_once()
    fn_Scatter.assert_called()


def test_plot_scatter_on_nav(mocker):
    result = create_backtest([ST, ], dfs,
                             start='2020-01-01', window=30).run()['ST']
    fn_Figure = mocker.patch(
        'btbox.backtest.results.selected.utils.Figure')
    fn_Scatter = mocker.patch(
        'btbox.backtest.results.selected.utils.Scatter')
    result.journals['every-2d', 'every-5d'].plot_scatter_on_nav()
    fn_Figure.assert_called_once()
    fn_Scatter.assert_called()


def test_plot_scatter_on_price(mocker):
    result = create_backtest([ST, ], dfs,
                             start='2020-01-01', window=30).run()['ST']
    fn_Figure = mocker.patch(
        'btbox.backtest.results.selected.utils.Figure')
    fn_Scatter = mocker.patch(
        'btbox.backtest.results.selected.utils.Scatter')
    result.journals['every-2d', 'every-5d'].plot_scatter_on_price('SPY')
    fn_Figure.assert_called_once()
    fn_Scatter.assert_called()


def test_plot_line_under_nav(mocker):
    result = create_backtest([ST, ], dfs,
                             start='2020-01-01', window=30).run()['ST']
    fn_make_subplots = mocker.patch(
        'btbox.backtest.results.selected.utils.make_subplots')
    fn_Scatter = mocker.patch(
        'btbox.backtest.results.selected.utils.Scatter')
    result.journals['line-8888', 'line-9999'].plot_line_under_nav()
    fn_make_subplots.assert_called_once()
    fn_Scatter.assert_called()


def test_plot_line_under_price(mocker):
    result = create_backtest([ST, ], dfs,
                             start='2020-01-01', window=30).run()['ST']
    fn_make_subplots = mocker.patch(
        'btbox.backtest.results.selected.utils.make_subplots')
    fn_Scatter = mocker.patch(
        'btbox.backtest.results.selected.utils.Scatter')
    result.journals['line-8888', 'line-9999'].plot_line_under_price('SPY')
    fn_make_subplots.assert_called_once()
    fn_Scatter.assert_called()


def test_plot_scatter_under_nav(mocker):
    result = create_backtest([ST, ], dfs,
                             start='2020-01-01', window=30).run()['ST']
    fn_make_subplots = mocker.patch(
        'btbox.backtest.results.selected.utils.make_subplots')
    fn_Scatter = mocker.patch(
        'btbox.backtest.results.selected.utils.Scatter')
    result.journals['every-2d', 'every-5d'].plot_scatter_under_nav()
    fn_make_subplots.assert_called_once()
    fn_Scatter.assert_called()
