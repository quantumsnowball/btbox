from btbox import create_job
from btbox.broker import Broker
from btbox.strategy import Strategy
from btbox.strategy.decorator import interval
from btbox.datasource.utils import import_yahoo_csv
import logging


logger = logging.getLogger()
logger.setLevel(logging.INFO)


def test_buy_stock():
    SYMBOL = 'SPY'
    QUANTITY = 10
    dfs = {SYMBOL: import_yahoo_csv('tests/_data_/SPY_bar1day.csv')}

    class S1(Strategy):
        name = 'test buy stock'

        def step(self, i: int, b: Broker):
            if i == 0:
                assert b.cash == 1e6
                b.order.trade(SYMBOL, +QUANTITY)
                b.order.withdrawal(b.cash)
                assert b.cash == 0
            if i % 1000 == 0 and i > 0:
                logger.info(dict(i=i, now=b.now, SPY=b.positions[SYMBOL]))
                assert b.positions[SYMBOL] == QUANTITY
                assert b.market.get_close(SYMBOL) * QUANTITY == \
                    b.audit.nav_account()

    s1_nav = create_job(S1, dfs).run().report.nav[-1]

    class S2(Strategy):
        name = 'test buy stock with decorator'

        def initial(self, b: Broker):
            assert b.cash == 1e6
            b.order.trade(SYMBOL, +QUANTITY)
            b.order.withdrawal(b.cash)
            assert b.cash == 0

        @interval(1000, initial=False)
        def step(self, b: Broker):
            logger.info(dict(now=b.now, SPY=b.positions[SYMBOL]))
            assert b.positions[SYMBOL] == QUANTITY
            assert b.market.get_close(SYMBOL) * QUANTITY == \
                b.audit.nav_account()

    s2_nav = create_job(S2, dfs).run().report.nav[-1]

    assert s1_nav == s2_nav
