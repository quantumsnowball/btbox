from typing import Any
from pandas import Series
import plotly.express as px


class Nav:
    def __init__(self,
                 name: str,
                 nav: Series) -> None:
        self._name = name
        self._nav = nav

    def plot(self, **kwargs_line: Any) -> None:
        if 'title' not in kwargs_line:
            kwargs_line['title'] = self._name
        fig = px.line(self._nav, **kwargs_line)
        fig.show()
