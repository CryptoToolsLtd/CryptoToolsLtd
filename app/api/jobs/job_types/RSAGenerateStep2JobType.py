from .JobType import JobType
from typing import override
from crypto import is_prime, random_prime, gcd # type: ignore

class RSAGenerateStep2JobType(JobType):
    @override
    def __init__(self):
        super().__init__(job_type="RSAGenerateStep2", immediate=True)
    
    @override
    def __call__(self, input: str) -> str:
        p, q, numBitsE = map(int, input.split(','))
        if not is_prime(p):
            raise ValueError("p is not prime")
        if not is_prime(q):
            raise ValueError("q is not prime")

        if numBitsE < 1:
            raise ValueError("Number of bits of e must be at least 1")
        phi_n = (p - 1) * (q - 1)
        if numBitsE >= phi_n.bit_length() or 2 ** numBitsE >= phi_n:
            raise ValueError("Number of bits of e is too large")
        
        while True:
            e = random_prime(lbound=f"{numBitsE}b", ubound=f"{numBitsE+2}b")
            if gcd(e, phi_n) == 1 and e < phi_n:
                break
        return str(e)
