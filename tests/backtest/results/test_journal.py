from btbox.broker import Broker
from btbox.strategy import Strategy
from btbox.datasource.utils import import_yahoo_csv
from btbox.backtest.utils import create_backtest


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


def mock_Figure_Scatter(fn_test):
    def wrapper(mocker):
        fn_Figure = mocker.patch(
            'btbox.backtest.results.selected.utils.Figure')
        fn_Scatter = mocker.patch(
            'btbox.backtest.results.selected.utils.Scatter')
        fn_test()
        fn_Figure.assert_called_once()
        fn_Scatter.assert_called()
    return wrapper


def mock_make_subplots_Scatter(fn_test):
    def wrapper(mocker):
        fn_make_subplots = mocker.patch(
            'btbox.backtest.results.selected.utils.make_subplots')
        fn_Scatter = mocker.patch(
            'btbox.backtest.results.selected.utils.Scatter')
        fn_test()
        fn_make_subplots.assert_called_once()
        fn_Scatter.assert_called()
    return wrapper


def make_ST_result(fn_test):
    def wrapper():
        result = create_backtest([ST, ], dfs,
                                 start='2020-01-01', window=30).run()['ST']
        fn_test(result)
    return wrapper


@make_ST_result
def test_bfill_ffill(result):
    df_pre = result.journals['point-1111'].values
    df_bfill = result.journals['point-1111'].bfill.values
    assert df_bfill.equals(df_pre.bfill())
    df_pre = result.journals['point-2222'].values
    df_ffill = result.journals['point-2222'].ffill.values
    assert df_ffill.equals(df_pre.ffill())


@mock_Figure_Scatter
@make_ST_result
def test_plot_line(result):
    result.journals['line-8888', 'line-9999'].plot_line()


@mock_Figure_Scatter
@make_ST_result
def test_plot_scatter(result):
    assert result.journals['every-2d', 'every-5d'].values.shape[1] == 2
    assert result.journals['every-2d', 'every-4d'].values.shape[1] == 2
    result.journals['every-2d', 'every-5d'].plot_scatter()


@mock_Figure_Scatter
@make_ST_result
def test_plot_line_on_price(result):
    result.journals['line-8888', 'line-9999'].plot_line_on_price('SPY')


@mock_Figure_Scatter
@make_ST_result
def test_plot_scatter_on_nav(result):
    result.journals['every-2d', 'every-5d'].plot_scatter_on_nav()


@mock_Figure_Scatter
@make_ST_result
def test_plot_scatter_on_price(result):
    result.journals['every-2d', 'every-5d'].plot_scatter_on_price('SPY')


@mock_make_subplots_Scatter
@make_ST_result
def test_plot_line_under_nav(result):
    result.journals['line-8888', 'line-9999'].plot_line_under_nav()


@mock_make_subplots_Scatter
@make_ST_result
def test_plot_line_under_price(result):
    result.journals['line-8888', 'line-9999'].plot_line_under_price('SPY')


@mock_make_subplots_Scatter
@make_ST_result
def test_plot_scatter_under_nav(result):
    result.journals['every-2d', 'every-5d'].plot_scatter_under_nav()
