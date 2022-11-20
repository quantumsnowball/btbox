from typing import Callable, Iterable
from pandas import DataFrame
from btbox.strategy.journal import Journal
from functools import wraps
import plotly.express as px


class FilteredMarks:
    def __init__(self,
                 name: str,
                 filtered: DataFrame) -> None:
        self._name = name
        self._filtered = filtered

    @staticmethod
    def set_default_title(func) -> Callable[..., None]:
        @wraps(func)
        def wrapped(self, *args, **kwargs) -> None:
            if 'title' not in kwargs:
                kwargs['title'] = self._name
            return func(self, *args, **kwargs)
        return wrapped

    @property
    def values(self) -> DataFrame:
        return self._filtered

    @set_default_title
    def plot_line(self, **line_kws) -> None:
        if 'title' not in line_kws:
            line_kws['title'] = self._name
        fig = px.line(self._filtered, **line_kws)
        fig.show()


class Journals:
    def __init__(self,
                 name: str,
                 journal: Journal) -> None:
        self._name = name
        self._marks = journal.marks

    def __getitem__(self, names: Iterable[str]):
        df = self._marks.loc[:, names]
        return FilteredMarks(self._name, df)
