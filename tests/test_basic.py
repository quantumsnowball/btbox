import btbox
import btbox.strategy
import btbox.backtest


class Algo(btbox.Strategy):
    name = 'Algo'

    def step(self):
        # this contains the algo logics
        pass


def test1():
    btbox.create_backtest(Algo).run()


def test2():
    btbox.backtest.create(Algo).run()
