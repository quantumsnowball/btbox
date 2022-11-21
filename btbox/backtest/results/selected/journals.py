from typing import Any, Callable, Iterable, ParamSpec, TypeVar
from pandas import DataFrame, Series
from plotly.graph_objects import Figure, Scatter
from btbox.strategy.journal import Journal
from functools import wraps
import plotly.express as px
from plotly.subplots import make_subplots


P = ParamSpec('P')
R = TypeVar('R')


class FilteredMarks:
    def __init__(self,
                 name: str,
                 nav: Series,
                 filtered: DataFrame) -> None:
        self._name = name
        self._nav = nav
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
    def plot_line(self, **kwargs_line: Any) -> None:
        fig = px.line(self._filtered, **kwargs_line)
        fig.show()

    @set_default_title
    def plot_scatter(self, **kwargs_scatter: Any) -> None:
        fig = px.scatter(self._filtered, **kwargs_scatter)
        fig.show()

    def plot_scatter_on_nav(self) -> None:
        fig = Figure()
        fig.add_trace(Scatter(x=self._nav.index,
                              y=self._nav))
        for _, sr in self._filtered.items():
            points = self._nav[~sr.isnull()]
            fig.add_trace(
                Scatter(
                    mode='markers',
                    x=points.index,
                    y=points,
                    marker=dict(size=10)))
        fig.show()

    def plot_line_under_nav(self) -> None:
        fig = make_subplots(rows=2, shared_xaxes=True)
        fig.add_trace(Scatter(x=self._nav.index,
                              y=self._nav), row=1, col=1)
        for _, sr in self._filtered.items():
            fig.add_trace(Scatter(x=sr.index,
                                  y=sr), row=2, col=1)
        fig.show()

    def plot_scatter_under_nav(self) -> None:
        fig = make_subplots(rows=2, shared_xaxes=True)
        fig.add_trace(Scatter(x=self._nav.index,
                              y=self._nav), row=1, col=1)
        for _, sr in self._filtered.items():
            fig.add_trace(
                Scatter(
                    mode='markers',
                    x=sr.index,
                    y=sr,
                    marker=dict(size=10)),
                row=2, col=1)
        fig.show()


class Journals:
    def __init__(self,
                 name: str,
                 nav: Series,
                 journal: Journal) -> None:
        self._name = name
        self._nav = nav
        self._marks = journal.marks

    def __getitem__(self, names: Iterable[str]) -> FilteredMarks:
        df = self._marks.loc[:, names]
        return FilteredMarks(self._name, self._nav, df)
