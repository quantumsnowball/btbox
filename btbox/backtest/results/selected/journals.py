from typing import Any, Callable, Iterable, ParamSpec, TypeVar
from pandas import DataFrame
from btbox.strategy.journal import Journal
from functools import wraps
import plotly.express as px


P = ParamSpec('P')
R = TypeVar('R')


class FilteredMarks:
    def __init__(self,
                 name: str,
                 filtered: DataFrame) -> None:
        self._name = name
        self._filtered = filtered

    @staticmethod
    def set_default_title(fn_plot: Callable[P, R]) -> Callable[P, R]:
        @wraps(fn_plot)
        def wrapped(*args: P.args,
                    **kwargs: P.kwargs) -> R:
            if isinstance(args[0], FilteredMarks):
                if 'title' not in kwargs:
                    kwargs['title'] = args[0]._name
            return fn_plot(*args, **kwargs)
        return wrapped

    @property
    def values(self) -> DataFrame:
        return self._filtered

    @set_default_title
    def plot_line(self, **line_kws: Any) -> None:
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
