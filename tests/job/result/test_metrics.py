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
        # BTC_bar1min=(365 * 24 * 60, 180),
        BTC_bar1hour=(365 * 24, 30),
        BTC_bar1day=(365, 3),
        SPY_bar1day=(252, 3),
        SPY_bar1week=(52, 0.4),
        SPY_bar1month=(12, 0.1),
    )
    for fn, (exp, err) in test_cases.items():
        ts = import_yahoo_csv(f'tests/_data_/{fn}.csv')
        af = Mt.detect_annualize_factor(ts)
        assert exp - err < af < exp + err

    # bar1day = import_yahoo_csv('tests/_data_/SPY_bar1day.csv')
    # bar1week = import_yahoo_csv('tests/_data_/SPY_bar1week.csv')
    # bar1month = import_yahoo_csv('tests/_data_/SPY_bar1month.csv')
    # af1day = Mt.detect_annualize_factor(bar1day)
    # af1week = Mt.detect_annualize_factor(bar1week)
    # af1month = Mt.detect_annualize_factor(bar1month)
    # assert 0


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
