from .JobType import JobType
from typing import override
from crypto import generate_elliptic_curve_with_number_of_points_being_prime # type: ignore
from random import randrange

class ECGenerateJobType(JobType):
    @override
    def __init__(self):
        super().__init__(job_type="ECGenerate", immediate=False)
    
    @override
    def __call__(self, input: str) -> str:
        numBitsP = int(input)
        if numBitsP < 1:
            raise ValueError("Invalid number of bits of p")
        if numBitsP > 256:
            raise ValueError("Number of bits of p is too large")
        
        ec = generate_elliptic_curve_with_number_of_points_being_prime(numBitsP)

        p, a, b = ec.p, ec.a, ec.b
        Px, Py = ec.starting_point
        s = randrange(min(4000, max(2, p // 2)), p)

        return f"{p},{a},{b},{Px},{Py},{s}"
