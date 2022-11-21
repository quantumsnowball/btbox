from typing import Any
from pandas import Series
import plotly.express as px


class Nav:
    def __init__(self,
                 name: str,
                 nav: Series) -> None:
        self._name = name
        self._nav = nav

    def plot(self, **line_kws: Any) -> None:
        if 'title' not in line_kws:
            line_kws['title'] = self._name
        fig = px.line(self._nav, **line_kws)
        fig.show()
