from .JobType import JobType
from typing import override
from random import randrange
from crypto import gcd # type: ignore

class ElGamalSignatureGenerateKJobType(JobType):
    @override
    def __init__(self):
        super().__init__(job_type="ElGamalSignatureGenerateK", immediate=True)
    
    @override
    def __call__(self, input: str) -> str:
        p = int(input)
        p_minus_1 = p - 1
        while True:
            k = randrange(1, p_minus_1)
            if gcd(k, p_minus_1) == 1:
                return str(k)
