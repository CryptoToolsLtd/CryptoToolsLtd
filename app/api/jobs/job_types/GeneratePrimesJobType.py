from .JobType import JobType
from typing import override
from crypto import random_prime_fast # type: ignore

class GeneratePrimesJobType(JobType):
    @override
    def __init__(self):
        super().__init__(job_type="Generate Primes", immediate=False)
    
    @override
    def __call__(self, input: str) -> str:
        num_bits, takes, want_p_congruent_to_3_mod_4 = input.split(',')
        n = int(num_bits)
        s = int(takes)
        w3m4 = want_p_congruent_to_3_mod_4 == "true"
        output = random_prime_fast(f"{n}b", f"{n+2}b", s, want_p_congruent_to_3_mod_4=w3m4)
        return ','.join(map(str, output))
