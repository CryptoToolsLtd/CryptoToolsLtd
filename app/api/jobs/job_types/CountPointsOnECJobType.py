from .JobType import JobType
from typing import override
from crypto import count_points_on_curve_with_prime_modulo # type: ignore

class CountPointsOnECJobType(JobType):
    @override
    def __init__(self):
        super().__init__(job_type="Count Points on EC", immediate=True)
    
    @override
    def __call__(self, input: str) -> str:
        p, a, b = map(lambda x: int(x), input.split(','))
        if p.bit_length() > 21:
            raise ValueError("p is too large ; we don't use Schoof so we can't handle it")
        output = count_points_on_curve_with_prime_modulo(p, a, b)
        return str(output)
