from pandas import DataFrame, Series
from plotly.graph_objects import Figure, Scatter


def make_single_simple_fig(df: DataFrame,
                           *,
                           title: str,
                           scatter: bool = False,
                           log_y: bool = True) -> Figure:
    fig = Figure()
    fig.update_layout(title=title)
    if log_y:
        fig.update_yaxes(type='log')
    for name, sr in df.items():
        fig.add_trace(
            Scatter(
                mode='markers' if scatter else 'lines',
                name=name,
                x=sr.index,
                y=sr))
    return fig


def make_top_and_bottom_fig(data_top: Series,
                            data_bottom: DataFrame,
                            *,
                            log_y: bool = True) -> Figure:
    fig = Figure()
    return fig
