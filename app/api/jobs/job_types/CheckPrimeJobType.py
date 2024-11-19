from .JobType import JobType
from typing import override
from crypto import is_prime # type: ignore

class CheckPrimeJobType(JobType):
    @override
    def __init__(self):
        super().__init__(job_type="Check Prime", immediate=True)
    
    @override
    def __call__(self, input: str) -> str:
        a = int(input)
        output = is_prime(a)
        if output:
            return "true"
        else:
            return "false"
