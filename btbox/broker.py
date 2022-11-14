class Broker:
    def __init__(self):
        self._cash = 0
        self._position = {}

    # operations
    def deposit(self,
                amount: float):
        self._cash += amount

    def trade(self,
              ticker: str,
              amount: float):
        pass
