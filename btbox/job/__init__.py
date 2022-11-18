from btbox.share import Clock
from btbox.job.result import Result
from btbox.strategy import Strategy


class Job:
    def __init__(self,
                 strategy: Strategy,
                 clock: Clock) -> None:
        assert isinstance(strategy, Strategy)
        self._strategy = strategy
        self._broker = self._strategy.broker
        self._timeline = self._strategy.timeline
        self._clock = clock

    def run(self) -> Result:
        # initialize clock
        self._clock.sync(self._timeline[0], self)
        # run the start function
        self._strategy.initial(self._broker)
        # timeline loop
        for i, now in enumerate(self._timeline):
            # set now and sync across all objects
            self._clock.sync(now, self)
            # run strategy as defined by user
            self._strategy.step(i, self._broker)
            # do daily settlement
            self._broker.settlement()
        return Result(self._strategy, self._broker.report)
