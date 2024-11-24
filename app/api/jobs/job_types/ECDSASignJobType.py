from .JobType import JobType
from typing import override
from crypto import is_prime, str2int, EllipticCurve, inverse # type: ignore

class ECDSASignJobType(JobType):
    @override
    def __init__(self):
        super().__init__(job_type="ECDSASign", immediate=True)
    
    @override
    def __call__(self, input: str) -> str:
        p, a, b, gx, gy, n, d, k, message_type, message = input.split(',')
        p, a, b, gx, gy, n, d, k = map(lambda x: int(x), (p, a, b, gx, gy, n, d, k))
        p_is_prime = (is_prime(p) is not False)
        if not p_is_prime:
            raise NotImplementedError("The case that p is not prime is not supported yet")

        if message_type == "text":
            m = str2int(str(message))
        else:
            m = int(message)
        
        ec = EllipticCurve(p, p_is_prime, a, b, (gx, gy))
        G = ec.starting_point

        x1, y1 = ec.scale_point(k, G)
        r = x1 % n
        
        h = m # maybe SHA-512 here
        one_per_k_mod_n = inverse(k, n)
        if one_per_k_mod_n is None:
            raise RuntimeError(f"Could not find the inverse of k mod n. Please choose another k.")

        s = (h + d * r) % n * one_per_k_mod_n % n
        
        if r == 0 or s == 0:
            raise RuntimeError(f"You falled into the case that r or s is 0. Please choose another value of k.")
        
        return f"{m},{x1},{y1},{r},{h},{s}"
