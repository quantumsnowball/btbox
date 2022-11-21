from typing import Callable, Iterable
from pandas import DataFrame
from btbox.strategy.journal import Journal
from functools import wraps
import plotly.express as px


T_fn_plot = Callable[..., None]
R_set_default_title = Callable[[T_fn_plot], None]


class FilteredMarks:
    def __init__(self,
                 name: str,
                 filtered: DataFrame) -> None:
        self._name = name
        self._filtered = filtered

    @staticmethod
    def set_default_title(fn_plot: T_fn_plot) -> R_set_default_title:
        @wraps(fn_plot)
        def wrapped(self, **kwargs) -> None:
            if 'title' not in kwargs:
                kwargs['title'] = self._name
            return fn_plot(self, **kwargs)
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

    def __getitem__(self, names: Iterable[str]) -> FilteredMarks:
        df = self._marks.loc[:, names]
        return FilteredMarks(self._name, df)
