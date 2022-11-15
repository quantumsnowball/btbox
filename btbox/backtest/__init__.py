from btbox.clock import Clock
from btbox.backtest.result import Result
from btbox.strategy import Strategy


class Backtest:
    def __init__(self,
                 strategy: Strategy,
                 clock: Clock) -> None:
        assert isinstance(strategy, Strategy)
        self._strategy = strategy
        self._broker = self._strategy.broker
        self._timeline = self._strategy.timeline
        self._clock = clock

    def run(self) -> Result:
        # timeline loop
        for i, now in enumerate(self._timeline):
            # set now and sync across all objects
            self._clock.now = now
            # run strategy as defined by user
            self._strategy.step(i, now, self._broker)
            # do daily settlement
            self._broker.settlement()
        return Result(self._strategy, self._broker.report)
