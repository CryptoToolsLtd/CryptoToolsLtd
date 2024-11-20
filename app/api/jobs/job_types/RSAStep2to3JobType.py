from .JobType import JobType
from typing import override
from crypto import is_prime, inverse # type: ignore

class RSAStep2To3JobType(JobType):
    @override
    def __init__(self):
        super().__init__(job_type="RSAStep2To3", immediate=True)
    
    @override
    def __call__(self, input: str) -> str:
        p, q, e = map(lambda x: int(x), input.split(','))
        if not is_prime(p):
            raise ValueError("p is not prime")
        if not is_prime(q):
            raise ValueError("q is not prime")
        
        phi_n = (p - 1) * (q - 1)
        if e < 1 or e >= phi_n:
            raise ValueError("e must be at least 1 and less than ϕ(n)")
        d = inverse(e, phi_n)
        if d is None:
            raise ValueError("e is not invertible. Choose e such that gcd(e, ϕ(n)) = 1")
        
        return str(d)
