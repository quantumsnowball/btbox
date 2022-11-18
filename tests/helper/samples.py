from btbox.broker import Broker
from btbox.strategy import Strategy
from btbox.strategy.decorator import interval


class BasicStepOnly(Strategy):

    def step(self, i: int, b: Broker):
        pass


class BasicInitialOnly(Strategy):

    def initial(self, b: Broker):
        pass


class BasicFullInterval10(Strategy):
    def initial(self, b: Broker):
        pass

    @interval(10)
    def step(self, b: Broker):
        pass
