from typing import Any
from btbox.job.result import Result
import plotly.express as px


class Nav:
    def __init__(self,
                 name: str,
                 result: Result) -> None:
        self._name = name
        self._result = result
        self._nav = self._result.report.nav

    def plot(self, **kwargs_line: Any) -> None:
        if 'title' not in kwargs_line:
            kwargs_line['title'] = self._name
        fig = px.line(self._nav, **kwargs_line)
        fig.show()
