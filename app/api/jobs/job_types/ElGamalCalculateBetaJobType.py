from .JobType import JobType
from typing import override
from crypto import modpower, is_primitive_root_fast # type: ignore
from .elgamal_tools import elgamal_check_p_certificate

class ElGamalCalculateBetaJobType(JobType):
    @override
    def __init__(self):
        super().__init__(job_type="ElGamalCalculateBeta", immediate=True)
    
    @override
    def __call__(self, input: str) -> str:
        p_as_str, alpha_as_str, a_as_str, p_certificate = input.split(',')
        p, alpha, a = map(int, (p_as_str, alpha_as_str, a_as_str))
        fact_of_p_minus_1 = elgamal_check_p_certificate(p, p_certificate)

        if not is_primitive_root_fast(alpha, p, fact_of_p_minus_1):
            raise ValueError("Invalid alpha - it must be a primitive root modulo p.")

        beta = modpower(alpha, a, p)
        return str(beta)
