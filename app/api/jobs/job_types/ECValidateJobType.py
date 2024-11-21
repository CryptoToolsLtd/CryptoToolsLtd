from .JobType import JobType
from typing import override
from crypto import is_prime, EllipticCurve # type: ignore

class ECValidateJobType(JobType):
    @override
    def __init__(self):
        super().__init__(job_type="ECValidate", immediate=False)
    
    @override
    def __call__(self, input: str) -> str:
        p, a, b, Px, Py, s = map(int, input.split(","))
        p_is_prime = (is_prime(p) is not False)
        if p < 2 or not p_is_prime:
            raise ValueError("Invalid p")
        # if a < 0 or a >= p:
        #     raise ValueError("Invalid a")
        # if b < 0 or b >= p:
        #     raise ValueError("Invalid b")
        # if Px < 0 or Px >= p:
        #     raise ValueError("Invalid Px")
        # if Py < 0 or Py >= p:
        #     raise ValueError("Invalid Py")
        # if s < 0 or s >= p:
        #     raise ValueError("Invalid s")
        
        if (4 * a ** 3 + 27 * b ** 2) % p == 0:
            raise ValueError("Invalid curve")
        
        if (Py ** 2 - Px ** 3 - a * Px - b) % p != 0:
            raise ValueError("Invalid point")
        
        ec = EllipticCurve(p, p_is_prime, a, b, (Px, Py))
        Bx, By = ec.get_point_by_index(s)
        return f"{Bx},{By}"
