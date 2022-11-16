from btbox.share import Clock
from btbox.broker.audit import Audit
from btbox.broker.order import Order
from btbox.market import Market


class Portfolio:
    def __init__(self,
                 order: Order,
                 market: Market,
                 audit: Audit,
                 clock: Clock):
        self._order = order
        self._market = market
        self._audit = audit
        self._clock = clock

    def trade_target_weight(self,
                            symbol: str,
                            target_weight: float,
                            min_weight: float = 0.001) -> None:
        nav = self._audit.nav_account()
        target_value = nav * target_weight
        net_value = target_value - self._audit.nav_position(symbol)
        if abs(net_value / nav) < min_weight:
            return
        target_quantity = net_value / \
            self._market.get_close_at(symbol, self._clock.now)
        self._order.trade(symbol, target_quantity)
