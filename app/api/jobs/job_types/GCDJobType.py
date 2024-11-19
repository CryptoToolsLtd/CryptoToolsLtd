from .JobType import JobType
from typing import override
from crypto import extended_euclidean # type: ignore

class GCDJobType(JobType):
    @override
    def __init__(self):
        super().__init__(job_type="GCD", immediate=True)
    
    @override
    def __call__(self, input: str) -> str:
        a, b = map(lambda x: int(x), input.split(','))
        d, inv, x0, y0 = extended_euclidean(a, b)
        R = b // d
        S = a // d
        return f"{d},{inv},{x0},{y0},{R},{S}"
