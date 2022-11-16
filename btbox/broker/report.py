from datetime import datetime
from pandas import DataFrame, Series


class _Record:
    class Nav:
        name = 'NAV'
        columns = ('Date', 'NAV')
        type = tuple[datetime, float]

    class Trades:
        name = 'Trades'
        columns = ('Date Symbol Action Quantity '
                   'Price GrossProceeds Fees NetProceeds').split(' ')
        type = tuple[datetime, str, str, float,
                     float, float, float, float]


class Report:
    def __init__(self) -> None:
        self._nav_log: list[_Record.Nav.type] = []
        self._trades_log: list[_Record.Trades.type] = []

    @property
    def nav(self) -> Series:
        df = DataFrame(self._nav_log,
                       columns=_Record.Nav.columns)
        return Series(df.NAV.values,
                      index=df.Date,
                      name=_Record.Nav.columns[-1])

    def log_nav(self, date: datetime, nav: float) -> None:
        self._nav_log.append((date, nav, ))

    @property
    def trades(self) -> DataFrame:
        df = DataFrame(self._trades_log,
                       columns=_Record.Trades.columns)
        df.set_index('Date', inplace=True)
        return df

    def log_trade(
        self, date: datetime, symbol: str, action: str, quantity: float,
        price: float, gross_proceeds: float, fees: float, net_proceeds: float
    ) -> None:
        self._trades_log.append((
            date, symbol, action, quantity,
            price, gross_proceeds, fees, net_proceeds, ))
