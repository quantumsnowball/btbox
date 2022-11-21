from btbox.broker import Broker
from btbox.strategy import Strategy
from btbox.datasource.utils import import_yahoo_csv
from btbox.backtest.utils import create_backtest
from btbox.strategy.decorator import interval


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
    fn_line = mocker.patch('btbox.backtest.results.selected.journals.px.line')
    result.journals['line-8888', 'line-9999'].plot_line()
    fn_line.assert_called_once()


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
    fn_scatter = mocker.patch(
        'btbox.backtest.results.selected.journals.px.scatter')
    result.journals['Every 2 Days', 'Every 5 Days'].plot_scatter()
    fn_scatter.assert_called_once()

    # results['MarkMe'].journal['MACD(3,5,6)'].plot_under_nav()
    # results.journals['RSI(20)'].plot_under_benchmark()
    # results.chart['MarkMe'].marks.plot(overlay_nav=True)
