from functools import wraps
from typing import Any, Callable, TypeVar
from btbox.strategy import Strategy
from btbox.broker import Broker


St = TypeVar('St', bound=Strategy)
T_fn_step = Callable[[St, Broker], Any]
R_decorator = Callable[[St, int, Broker], Any]
R_interval = Callable[[T_fn_step], R_decorator]


def interval(n: int,
             *,
             initial: bool = True) -> R_interval:
    def decorator(fn_step: T_fn_step) -> R_decorator:
        @wraps(fn_step)
        def wrpfn_step(self,
                       i: int,
                       b: Broker) -> None:
            if i % n == 0:
                return fn_step(self, b)

        @wraps(fn_step)
        def wrpfn_step_skip_initial(self,
                                    i: int,
                                    b: Broker) -> None:
            if i % n == 0 and i > 0:
                return fn_step(self, b)

        return wrpfn_step if initial else wrpfn_step_skip_initial
    return decorator
