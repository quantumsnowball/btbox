from btbox.broker import Broker


def interval(n: int, *, initial: bool = True):
    def decorator(fn_step):
        def wrpfn_step(self, i: int, b: Broker):
            if i % n == 0:
                return fn_step(self, b)

        def wrpfn_step_skip_initial(self, i: int, b: Broker):
            if i % n == 0 and i > 0:
                return fn_step(self, b)

        return wrpfn_step if initial else wrpfn_step_skip_initial
    return decorator
