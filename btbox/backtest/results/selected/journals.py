from typing import Any, Callable, Iterable, ParamSpec, Self, TypeVar
from pandas import DataFrame
from plotly.graph_objects import Figure, Scatter
from btbox.backtest.results.selected.utils import make_single_overlay_fig, make_single_simple_fig
from btbox.job.result import Result
from btbox.strategy.journal import Journal
from functools import wraps
import plotly.express as px
from plotly.subplots import make_subplots


P = ParamSpec('P')
R = TypeVar('R')


class FilteredMarks:
    def __init__(self,
                 name: str,
                 result: Result,
                 filtered: DataFrame) -> None:
        self._name = name
        self._result = result
        self._nav = self._result.report.nav
        self._filtered = filtered

    @property
    def bfill(self) -> Self:
        self._filtered = self._filtered.fillna(axis=0, method='bfill')
        return self

    @property
    def ffill(self) -> Self:
        self._filtered = self._filtered.fillna(axis=0, method='ffill')
        return self

    @staticmethod
    def set_default_title(name: str = 'title') \
            -> Callable[[Callable[P, R]], Callable[P, R]]:
        def wrapper_fn_plot(fn_plot: Callable[P, R]) -> Callable[P, R]:
            @wraps(fn_plot)
            def wrapped_fn_plot(*args: P.args,
                                **kwargs: P.kwargs) -> R:
                if isinstance(args[0], FilteredMarks):
                    if name not in kwargs:
                        kwargs[name] = args[0]._name
                return fn_plot(*args, **kwargs)
            return wrapped_fn_plot
        return wrapper_fn_plot

    @property
    def values(self) -> DataFrame:
        return self._filtered

    @set_default_title()
    def plot_line(self, **kwargs: Any) -> None:
        fig = make_single_simple_fig(self._filtered, **kwargs)
        fig.show()

    @set_default_title()
    def plot_scatter(self, **kwargs: Any) -> None:
        fig = make_single_simple_fig(
            self._filtered, scatter=True, log_y=False, **kwargs)
        fig.show()

    @set_default_title()
    def plot_scatter_on_nav(self, **kwargs: Any) -> None:
        fig = make_single_overlay_fig(
            self._nav, self._filtered, name_main='NAV', scatter=True, **kwargs)
        fig.show()

    @set_default_title()
    def plot_scatter_on_price(self,
                              symbol: str,
                              **kwargs: Any) -> None:
        price = self._result.datasource.get_dataframe(symbol).Close
        fig = make_single_overlay_fig(
            price, self._filtered, name_main=symbol, scatter=True, **kwargs)
        fig.show()

    @set_default_title()
    def plot_line_under_nav(self, **kwargs_update_layout: Any) -> None:
        fig = make_subplots(rows=2, shared_xaxes=True)
        fig.update_layout(**kwargs_update_layout)
        fig.add_trace(
            Scatter(
                name='NAV',
                x=self._nav.index,
                y=self._nav), row=1, col=1)
        for name, sr in self._filtered.items():
            fig.add_trace(
                Scatter(
                    name=name,
                    x=sr.index,
                    y=sr), row=2, col=1)
        fig.show()

    @set_default_title()
    def plot_line_under_price(self,
                              symbol: str,
                              **kwargs_update_layout: Any) -> None:
        price = self._result.datasource.get_dataframe(symbol).Close
        fig = make_subplots(rows=2, shared_xaxes=True)
        fig.update_layout(**kwargs_update_layout)
        fig.add_trace(
            Scatter(
                name=symbol,
                x=price.index,
                y=price), row=1, col=1)
        for name, sr in self._filtered.items():
            fig.add_trace(
                Scatter(
                    name=name,
                    x=sr.index,
                    y=sr), row=2, col=1)
        fig.show()

    @set_default_title()
    def plot_scatter_under_nav(self, **kwargs_update_layout: Any) -> None:
        fig = make_subplots(rows=2, shared_xaxes=True)
        fig.update_layout(**kwargs_update_layout)
        fig.add_trace(
            Scatter(
                name='NAV',
                x=self._nav.index,
                y=self._nav), row=1, col=1)
        for name, sr in self._filtered.items():
            fig.add_trace(
                Scatter(
                    mode='markers',
                    name=name,
                    x=sr.index,
                    y=sr,
                    marker=dict(size=10)),
                row=2, col=1)
        fig.show()


class Journals:
    def __init__(self,
                 name: str,
                 result: Result,
                 journal: Journal) -> None:
        self._name = name
        self._result = result
        self._nav = self._result.report.nav
        self._marks = journal.marks

    def __getitem__(self, names: Iterable[str]) -> FilteredMarks:
        df = DataFrame(self._marks.loc[:, names])
        return FilteredMarks(self._name, self._result, df)
