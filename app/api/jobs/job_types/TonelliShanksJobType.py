from .JobType import JobType
from typing import override
from crypto import find_sq_roots, is_prime # type: ignore

class TonelliShanksJobType(JobType):
    @override
    def __init__(self):
        super().__init__(job_type="Tonelli-Shanks", immediate=True)
    
    @override
    def __call__(self, input: str) -> str:
        p, a = map(int, input.split(','))
        p_is_prime_and_odd = is_prime(p) and p % 2 == 1
        if not p_is_prime_and_odd:
            raise NotImplementedError("p must be prime and odd ; other values of p are not supported yet.")
        solutions = find_sq_roots(a, p, p_is_prime_and_odd)
        return ",".join(map(str, solutions))
