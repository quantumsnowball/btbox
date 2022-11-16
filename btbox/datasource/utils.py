from datetime import datetime
from typing import Union, Tuple
from pandas import to_datetime, read_csv, DataFrame


class Parser:
    def __init__(self):
        pass


def parse_start_end_window(
        first_ohlcv: DataFrame,
        start: Union[datetime, str, None],
        end: Union[datetime, str, None],
        window: int) -> Tuple[datetime, datetime, int, datetime, datetime]:
    # None means min or max
    start = first_ohlcv.index[0] if not start else start
    end = first_ohlcv.index[-1] if not end else end
    # end must be greater than start
    start_: datetime = to_datetime(start)
    end_: datetime = to_datetime(end)
    assert start_ < end_
    # ensurefirst window size is correct
    window_ = max(window, 1)
    first_window: DataFrame = first_ohlcv.loc[:start_].iloc[-window_:]
    assert len(first_window) == window_
    # trim the window accordingly
    trim_from = first_window.index[0]
    trim_to = end_
    # return valid values
    return (start_, end_, window_, trim_from, trim_to)


def verify_ohlcv(ohlcv: DataFrame) -> DataFrame:
    # ensure the window has valid values
    assert isinstance(ohlcv, DataFrame)
    assert ohlcv.index.name == 'Date'
    assert ohlcv.columns.tolist() == ['Open', 'High', 'Low', 'Close', 'Volume']
    assert not ohlcv.isnull().values.any()
    assert not ohlcv.isna().values.any()
    return ohlcv


def trim_ohlcv_length(ohlcv: DataFrame,
                      trim_from: datetime,
                      trim_to: datetime) -> DataFrame:
    # trim dataframe by valid start and end
    ohlcv_trimmed = ohlcv.loc[trim_from: trim_to]
    # valid dataframe
    ohlcv_clean = verify_ohlcv(ohlcv_trimmed)
    return ohlcv_clean


def import_yahoo_csv(path: str) -> DataFrame:
    df = read_csv(path,
                  index_col='Date',
                  parse_dates=True)
    df.drop('Close', axis=1, inplace=True)
    df.rename({'Adj Close': 'Close'}, axis=1, inplace=True)
    return df
