from .JobType import JobType
from typing import override
from .elgamal_tools import elgamal_check_p_certificate
from crypto import is_primitive_root_fast, random_prime # type: ignore

class ElGamalGenerateAlphaAJobType(JobType):
    @override
    def __init__(self):
        super().__init__(job_type="ElGamalGenerateAlphaA", immediate=True)
    
    @override
    def __call__(self, input: str) -> str:
        p_as_str, p_certificate = input.split(",")
        p = int(p_as_str)

        fact_of_p_minus_1 = elgamal_check_p_certificate(p, p_certificate)

        alpha = 2
        while not is_primitive_root_fast(alpha, p, fact_of_p_minus_1):
            alpha += 1
        a = random_prime(lbound=p // 3, ubound=p - 1)

        return f"{alpha},{a},{p_certificate}"
