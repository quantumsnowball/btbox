from datetime import datetime
from pandas import Series
from pandas import to_datetime as dt
import btbox
import btbox.job
from btbox.broker import Broker
from btbox.datasource.utils import import_yahoo_csv
import btbox.job.result.metrics as Mt
import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)


def test_detect_annualize_factor():
    test_cases = dict(
        BTC_bar1min=365 * 24 * 60,
        BTC_bar3min=365 * 24 * 60 / 3,
        BTC_bar5min=365 * 24 * 60 / 5,
        BTC_bar15min=365 * 24 * 60 / 15,
        BTC_bar1hour=365 * 24,
        BTC_bar2hour=365 * 24 / 2,
        BTC_bar3hour=365 * 24 / 3,
        BTC_bar4hour=365 * 24 / 4,
        BTC_bar1day=365,
        BTC_bar1month=12,
        SPY_bar1day=252,
        SPY_bar1week=52,
        SPY_bar1month=12,
    )
    for filename, exp_val in test_cases.items():
        ts = import_yahoo_csv(f'tests/_data_/{filename}.csv')
        annualize_factor = Mt.detect_annualize_factor(ts)
        assert exp_val * 0.99 < annualize_factor < exp_val * 1.01


def test_total_return():
    assert Mt.total_return(Series([1, 1.5])) == 0.5
    assert Mt.total_return(Series([1, 2])) == 1.0
    assert Mt.total_return(Series([1] + list(range(20)) + [3])) == 2.0


def test_cagr():
    assert round(Mt.cagr(Series([1, 2], index=[
        dt('2020-01-01'), dt('2020-12-31')])), 4) == 1.0
    assert round(Mt.cagr(Series([1, 2], index=[
        dt('2020-01-01'), dt('2022-12-31')])), 4) == 0.2599
    assert round(Mt.cagr(Series([1, 2], index=[
        dt('2017-01-01'), dt('2022-12-31')])), 4) == 0.1225
    assert round(Mt.cagr(Series([1, 2], index=[
        dt('2013-01-01'), dt('2022-12-31')])), 4) == 0.0718


def test_mu_sigma():
    def confirm_similar_stats(fn_A, fn_B, err,
                              start=None, end=None):
        ts_A = import_yahoo_csv(
            f'tests/_data_/{fn_A}.csv').loc[start:end].Close
        ts_B = import_yahoo_csv(
            f'tests/_data_/{fn_B}.csv').loc[start:end].Close
        mu_A, sigma_A = Mt.mu_sigma(ts_A, Mt.detect_annualize_factor(ts_A))
        mu_B, sigma_B = Mt.mu_sigma(ts_B, Mt.detect_annualize_factor(ts_B))
        assert mu_A * (1 - err) < mu_B < mu_A * (1 + err)
        assert sigma_A * (1 - err) < sigma_B < sigma_A * (1 + err)
    confirm_similar_stats(
        'BTC_bar1min', 'BTC_bar5min', 0.05, '2022-11-10', '2022-11-15')
    confirm_similar_stats(
        'BTC_bar2hour', 'BTC_bar4hour', 0.05, '2021-01-01', '2021-12-31')
    confirm_similar_stats(
        'BTC_bar1day', 'BTC_bar1month', 0.08, '2015-01-01', '2022-10-30')
    confirm_similar_stats(
        'SPY_bar1day', 'SPY_bar1week', 0.07, '2010-01-01', '2021-12-31')
    confirm_similar_stats(
        'SPY_bar1week', 'SPY_bar1month', 0.13, '2010-01-01', '2021-12-31')


def test_sharpe():
    pass


def test_metrics():
    INI_CASH = 1e6
    SYMBOL = 'SPY'
    TARGET_WEIGHT = 1.0
    dataframes = {SYMBOL: import_yahoo_csv('tests/_data_/SPY_bar1day.csv')}

    class CustomStrategy(btbox.Strategy):
        name = 'test metrics'

        def step(self, i: int, now: datetime, broker: Broker):
            if i == 0:
                broker.order.deposit(INI_CASH)
                broker.portfolio.trade_target_weight(SYMBOL, TARGET_WEIGHT)
            if i % 1000 == 0:
                logger.info(dict(i=i, now=now, SPY=broker.positions[SYMBOL]))
                assert broker.report.trades.iloc[-1].Symbol == 'SPY'
                assert round(broker.audit.nav_account() * TARGET_WEIGHT) == \
                    round(broker.audit.nav_position(SYMBOL))

    job = btbox.create_job(CustomStrategy, dataframes)
    result = job.run()
    assert result.metrics.total_return == Mt.total_return(
        dataframes[SYMBOL].Close)
    assert result.metrics.cagr == Mt.cagr(
        dataframes[SYMBOL].Close)
    # assert result.metrics.mu == Mt.mu(
    #     dataframes[SYMBOL].Close)
