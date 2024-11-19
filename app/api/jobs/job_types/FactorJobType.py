from .JobType import JobType
from typing import override
from crypto import fact # type: ignore

class FactorJobType(JobType):
    @override
    def __init__(self):
        super().__init__(job_type="Factor", immediate=True)
    
    @override
    def __call__(self, input: str) -> str:
        a = int(input)
        output = fact(a)

        F = [
            f"({base}^{exponent})"
            for [base, exponent] in output.items()
        ]
        return 'x'.join(F)
