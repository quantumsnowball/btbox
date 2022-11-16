from typing import List
from btbox.backtest.results import Results
from btbox.job import Job


class Backtest:
    def __init__(self,
                 jobs: List[Job]) -> None:
        self._jobs = jobs

    def run(self) -> Results:
        results = []
        for job in self._jobs:
            result = job.run()
            results.append(result)
        return Results(results)
