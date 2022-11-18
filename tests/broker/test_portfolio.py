import btbox
import btbox.job
from btbox.broker import Broker
from btbox.datasource.utils import import_yahoo_csv
import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)


def test_target_weight():
    INI_CASH = 1e6
    SYMBOL = 'SPY'
    TARGET_WEIGHT = 0.5
    dataframes = {SYMBOL: import_yahoo_csv('tests/_data_/SPY_bar1day.csv')}

    class CustomStrategy(btbox.Strategy):
        name = 'test target weight'

        def step(self, i: int, broker: Broker):
            # initial deposit
            if i == 0:
                broker.order.deposit(INI_CASH)
            if i % 1000 == 0:
                broker.portfolio.trade_target_weight(
                    SYMBOL, TARGET_WEIGHT, min_weight=0)
                logger.info(dict(i=i, now=broker.now,
                            SPY=broker.positions[SYMBOL]))
                assert broker.report.trades.iloc[-1].Symbol == 'SPY'
                assert round(broker.audit.nav_account() * TARGET_WEIGHT) == \
                    round(broker.audit.nav_position(SYMBOL))

    btbox.create_job(CustomStrategy, dataframes).run()
