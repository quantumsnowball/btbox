from datetime import datetime


RISK_FREE_RATE = 0.0


class Clock:
    def __init__(self, now: datetime = datetime(1970, 1, 1)) -> None:
        self._now: datetime = now

    def _sync(self, now: datetime) -> None:
        self._now = now

    @property
    def now(self) -> datetime:
        return self._now
