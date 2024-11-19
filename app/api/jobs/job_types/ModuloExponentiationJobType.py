from .JobType import JobType
from typing import override
from crypto import modpower # type: ignore

class ModularExponentiationJobType(JobType):
    @override
    def __init__(self):
        super().__init__(job_type="Modular Exponentiation", immediate=True)
    
    @override
    def __call__(self, input: str) -> str:
        a, b, n = map(lambda x: int(x), input.split(','))
        output = modpower(a, b, n)
        return str(output)
