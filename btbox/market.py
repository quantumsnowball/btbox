import pandas as pd


class Market:
    def __init__(self, data):
        # check
        assert isinstance(data, pd.DataFrame)
        self._data = data
