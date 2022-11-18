from btbox import create_job
from btbox.broker import Broker
from btbox.strategy import Strategy
from btbox.datasource.utils import import_yahoo_csv
import logging


logger = logging.getLogger()
logger.setLevel(logging.INFO)


def test_nav_report():
    SYMBOL = 'SPY'
    QUANTITY = 10
    dataframes = {SYMBOL: import_yahoo_csv('tests/_data_/SPY_bar1day.csv')}

    class CustomStrategy(Strategy):
        name = 'test nav report'

        def step(self, i: int, b: Broker):
            if i == 0:
                assert b.cash == 1e6
            if i % 1000 == 0:
                b.order.trade(SYMBOL, +QUANTITY)
                logger.info(dict(i=i, now=b.now, SPY=b.positions[SYMBOL]))
                assert b.report.trades.iloc[-1].Symbol == 'SPY'
                assert b.report.trades.Quantity.sum() == \
                    (i // 1000 + 1) * QUANTITY

    create_job(CustomStrategy, dataframes).run()
