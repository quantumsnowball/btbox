from datetime import datetime
from typing import Any


RISK_FREE_RATE = 0.0


class Clock:
    def __init__(self,
                 Owner: type) -> None:
        self._now: datetime = datetime(1970, 1, 1)
        self._Owner = Owner

    def sync(self, now: datetime, caller: Any) -> None:
        assert isinstance(caller, self._Owner), \
            f'Only {self._Owner} is allowed to sync the clock.'
        self._now = now

    @property
    def now(self) -> datetime:
        return self._now
