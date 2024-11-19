from .JobType import JobType
from typing import override
from crypto import kronecker # type: ignore

class JKLJobType(JobType):
    @override
    def __init__(self):
        super().__init__(job_type="JKL", immediate=True)
    
    @override
    def __call__(self, input: str) -> str:
        a, b = map(lambda x: int(x), input.split(','))
        output = kronecker(a, b)
        return str(output)
