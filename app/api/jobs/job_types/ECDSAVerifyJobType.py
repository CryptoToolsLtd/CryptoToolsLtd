from .JobType import JobType
from typing import override
from crypto import is_prime, EllipticCurve, inverse # type: ignore

class ECDSAVerifyJobType(JobType):
    @override
    def __init__(self):
        super().__init__(job_type="ECDSAVerify", immediate=True)
    
    @override
    def __call__(self, input: str) -> str:
        p, a, b, gx, gy, n, Qx, Qy, m, r, s = map(int, input.split(',')) # type: ignore
        p_is_prime = (is_prime(p) is not False)
        if not p_is_prime:
            raise NotImplementedError("The case that p is not prime is not supported yet")

        ec = EllipticCurve(p, p_is_prime, a, b, (gx, gy))
        G = ec.starting_point

        h = m
        if r <= 0 or r >= n or s <= 0 or s >= n:
            return f"{h}`N/A`N/A`N/A`N/A`N/A`N/A`NO - r and s must be in the range of (0, n)."
        
        w = inverse(s, n)
        if w is None:
            return f"{h}`N/A`N/A`N/A`N/A`N/A`N/A`NO - Could not find w, the inverse of s mod n."
        
        u1 = h * w % n
        u2 = r * w % n
        x0, y0 = ec.add_points(ec.scale_point(u1, G), ec.scale_point(u2, (Qx, Qy)))
        v = x0 % n

        if v != r % n:
            verdict = "NO - because v != r (mod n)"
        else:
            verdict = "YES, message is authentic."
        
        return f"{h}`{w}`{u1}`{u2}`{x0}`{y0}`{v}`{verdict}"
