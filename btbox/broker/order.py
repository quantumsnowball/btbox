from btbox.broker.account import Account
from btbox.broker.report import Report
from btbox.market import Market


class Order:
    def __init__(self,
                 market: Market,
                 account: Account,
                 report: Report):
        self._market = market
        self._account = account
        self._report = report

    # system
    def sync(self, now) -> None:
        self._now = now

    def trade(self,
              symbol: str,
              quantity: float) -> None:
        # price
        price = self._market.get_close_at(symbol, self._now)
        # cash flow
        gross_proceeds = -price * quantity
        fees = 0
        net_proceeds = gross_proceeds - fees
        # settlement
        self._account.cash += net_proceeds
        self._account.positions[symbol] += quantity
        # write trade history
        self._report.log_trade(
            date=self._now, symbol=symbol,
            action='BOT' if quantity >= 0 else 'SLD', quantity=quantity,
            price=price, gross_proceeds=gross_proceeds, fees=fees,
            net_proceeds=net_proceeds)
