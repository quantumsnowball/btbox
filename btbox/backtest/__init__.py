from typing import List
from btbox.job import Job
from btbox.job.result import Result


class Backtest:
    def __init__(self,
                 jobs: List[Job]) -> None:
        self._jobs = jobs

    def run(self) -> List[Result]:
        results = []
        for job in self._jobs:
            result = job.run()
            results.append(result)
        return results
