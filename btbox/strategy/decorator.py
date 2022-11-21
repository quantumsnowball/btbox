from functools import wraps
from typing import Any, Callable, TypeVar
from btbox.strategy import Strategy
from btbox.broker import Broker


ST = TypeVar('ST', bound=Strategy)
T_fn_step = Callable[[ST, Broker], Any]
R_decorator = Callable[[ST, int, Broker], Any]
R_interval = Callable[[T_fn_step[ST]], R_decorator[ST]]


def interval(n: int,
             *,
             initial: bool = True) -> R_interval[ST]:
    def decorator(fn_step: T_fn_step[ST]) -> R_decorator[ST]:
        @wraps(fn_step)
        def wrpfn_step(self: ST,
                       i: int,
                       b: Broker) -> Any:
            if i % n == 0:
                return fn_step(self, b)

        @wraps(fn_step)
        def wrpfn_step_skip_initial(self: ST,
                                    i: int,
                                    b: Broker) -> Any:
            if i % n == 0 and i > 0:
                return fn_step(self, b)

        return wrpfn_step if initial else wrpfn_step_skip_initial
    return decorator
