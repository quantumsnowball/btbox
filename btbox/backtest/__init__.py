from btbox.backtest.results import Results
from btbox.job import Job


class Backtest:
    def __init__(self,
                 jobs: list[Job]) -> None:
        self._jobs = jobs
        assert len({j.name for j in self._jobs}) == len(self._jobs)

    def run(self) -> Results:
        results = []
        for job in self._jobs:
            result = job.run()
            results.append(result)
        return Results(results)
