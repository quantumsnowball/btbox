from btbox.broker import Broker
from btbox.strategy import Strategy
from btbox.datasource.utils import import_yahoo_csv
from btbox.backtest.utils import create_backtest
from numpy import isnan


def test_chart_marking():
    dfs = {'SPY': import_yahoo_csv('tests/_data_/SPY_bar1day.csv')}

    class S1(Strategy):
        name = 'MarkMe'

        def step(self, i: int, b: Broker):
            if i % 2 == 0 and i > 0:
                self.chart.mark(2, 'Every 2 Days')
            if i % 4 == 0 and i > 0:
                self.chart.mark(4, 'Every 4 Days')

    results = create_backtest(
        [S1, ], dfs, start='2020-01-01', window=30).run()
    dfm = results.strategies[0].chart.marks
    assert len(dfm) == len(results.strategies[0].timeline)
    assert dfm.shape[1] == 2
    assert isnan(dfm.iloc[0, 0]) and isnan(dfm.iloc[0, 1])
    assert isnan(dfm.iloc[1, 0]) and isnan(dfm.iloc[1, 1])
    assert dfm.iloc[2, 0] == 2 and isnan(dfm.iloc[2, 1])
    assert isnan(dfm.iloc[3, 0]) and isnan(dfm.iloc[3, 1])
    assert dfm.iloc[4, 0] == 2 and dfm.iloc[4, 1] == 4
    assert isnan(dfm.iloc[5, 0]) and isnan(dfm.iloc[5, 1])
    assert dfm.iloc[6, 0] == 2 and isnan(dfm.iloc[6, 1])
    # results.charts[0].plot_marks(nav=True)
    # results.chart.plot()
    # results.chart['MarkMe'].marks.plot(overlay_nav=True)
