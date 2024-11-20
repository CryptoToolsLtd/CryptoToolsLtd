from .JobType import JobType
from typing import override
from crypto import is_prime # type: ignore

class RSAStep1To2JobType(JobType):
    @override
    def __init__(self):
        super().__init__(job_type="RSAStep1To2", immediate=True)
    
    @override
    def __call__(self, input: str) -> str:
        p, q = map(lambda x: int(x), input.split(','))
        if not is_prime(p):
            raise ValueError("p is not prime")
        if not is_prime(q):
            raise ValueError("q is not prime")
        
        n = p * q
        p_1 = p - 1
        q_1 = q - 1
        phi_n = p_1 * q_1
        return f"{n},{p_1},{q_1},{phi_n}"
