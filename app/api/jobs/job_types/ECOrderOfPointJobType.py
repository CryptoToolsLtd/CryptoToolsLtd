from .JobType import JobType
from typing import override
from crypto import is_prime, EllipticCurve, calculate_order_of_point_on_curve # type: ignore

class ECOrderOfPointJobType(JobType):
    @override
    def __init__(self):
        super().__init__(job_type="ECOrderOfPoint", immediate=True)
    
    @override
    def __call__(self, input: str) -> str:
        p, a, b, gx, gy, Mx, My = map(lambda x: int(x), input.split(',')) # type: ignore
        p_is_prime = (is_prime(p) is not False)
        ec = EllipticCurve(p, p_is_prime, a, b, (gx, gy))
        result = calculate_order_of_point_on_curve(ec, (Mx, My))
        return f"{result}"
