from typing import Iterable
from pandas import DataFrame
from btbox.strategy.journal import Journal
import plotly.express as px


class FilteredMarks:
    def __init__(self,
                 name: str,
                 filtered: DataFrame) -> None:
        self._name = name
        self._filtered = filtered

    @property
    def values(self) -> DataFrame:
        return self._filtered

    def plot_line(self, **line_kws):
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
