from typing import Any, Callable, Iterable, ParamSpec, Self, TypeVar
from pandas import DataFrame
from btbox.backtest.results.selected.utils import (
    make_single_overlay_fig,
    make_single_simple_fig,
    make_top_and_bottom_fig)
from btbox.job.result import Result
from btbox.strategy.journal import Journal
from functools import wraps


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
    def default_title(fn_plot: Callable[P, R]) -> Callable[P, R]:
        @wraps(fn_plot)
        def wrapped_fn_plot(*args: P.args,
                            **kwargs: P.kwargs) -> R:
            if isinstance(args[0], FilteredMarks):
                if 'title' not in kwargs:
                    kwargs['title'] = args[0]._name
            return fn_plot(*args, **kwargs)
        return wrapped_fn_plot

    @property
    def values(self) -> DataFrame:
        return self._filtered

    @default_title
    def plot_line(self, **kwargs: Any) -> None:
        fig = make_single_simple_fig(self._filtered, **kwargs)
        fig.show()

    @default_title
    def plot_scatter(self, **kwargs: Any) -> None:
        fig = make_single_simple_fig(
            self._filtered, scatter=True, log_y=False, **kwargs)
        fig.show()

    @default_title
    def plot_scatter_on_nav(self, **kwargs: Any) -> None:
        fig = make_single_overlay_fig(
            self._nav, self._filtered, name_main='NAV', scatter=True, **kwargs)
        fig.show()

    @default_title
    def plot_scatter_on_price(self,
                              symbol: str,
                              **kwargs: Any) -> None:
        price = self._result.datasource.get_dataframe(symbol).Close
        fig = make_single_overlay_fig(
            price, self._filtered, name_main=symbol, scatter=True, **kwargs)
        fig.show()

    @default_title
    def plot_line_under_nav(self, **kwargs: Any) -> None:
        fig = make_top_and_bottom_fig(
            self._nav, self._filtered, name_top='NAV', ** kwargs)
        fig.show()

    @default_title
    def plot_line_under_price(self,
                              symbol: str,
                              **kwargs: Any) -> None:
        price = self._result.datasource.get_dataframe(symbol).Close
        fig = make_top_and_bottom_fig(
            price, self._filtered, name_top=symbol, ** kwargs)
        fig.show()

    @default_title
    def plot_scatter_under_nav(self, **kwargs: Any) -> None:
        fig = make_top_and_bottom_fig(
            self._nav, self._filtered, name_top='NAV', scatter=True, ** kwargs)
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
