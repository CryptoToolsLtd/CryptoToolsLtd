from .JobType import JobType
from typing import override
from crypto import ElGamal_generate_keypair # type: ignore
from .cert import issue_computation_cert
import json

class ElGamalGeneratePAlphaAJobType(JobType):
    @override
    def __init__(self):
        super().__init__(job_type="ElGamalGeneratePAlphaA", immediate=True)
    
    @override
    def __call__(self, input: str) -> str:
        numBitsP = int(input)
        if numBitsP < 1:
            raise ValueError("Invalid number of bits for p")
        if numBitsP > 2048:
            raise ValueError("Number of bits for p is too large")
        
        pubkey, privkey, fact_of_p_minus_1 = ElGamal_generate_keypair(numBitsP)
        p, alpha, _beta = pubkey
        a = privkey[1]
        p_certificate = issue_computation_cert("ElGamalGeneratePAlphaA", {
            "p": str(p),
            "fact_of_p_minus_1": json.dumps(fact_of_p_minus_1),
        })
        return f"{p},{alpha},{a},{p_certificate}"
