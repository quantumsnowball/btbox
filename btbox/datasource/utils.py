from pandas import read_csv, DataFrame


def verify_ohlcv(ohlcv: DataFrame) -> None:
    assert isinstance(ohlcv, DataFrame)
    assert ohlcv.index.name == 'Date'
    assert ohlcv.columns.tolist() == ['Open', 'High', 'Low', 'Close', 'Volume']
    assert not ohlcv.isnull().values.any()
    assert not ohlcv.isna().values.any()


def import_yahoo_csv(path: str) -> DataFrame:
    df = read_csv(path,
                  index_col='Date',
                  parse_dates=True)
    df.drop('Close', axis=1, inplace=True)
    df.rename({'Adj Close': 'Close'}, axis=1, inplace=True)
    return df
