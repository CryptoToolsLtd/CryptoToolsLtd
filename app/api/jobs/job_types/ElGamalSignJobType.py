from .JobType import JobType
from typing import override
from crypto import str2int, modpower, inverse # type: ignore
import json

class ElGamalSignJobType(JobType):
    @override
    def __init__(self):
        super().__init__(job_type="ElGamalSign", immediate=True)
    
    @override
    def __call__(self, input: str) -> str:
        try:
            raw_payload = json.loads(input)
            if not isinstance(raw_payload, dict):
                raise ValueError("Invalid JSON input")
            
        except:
            raise ValueError("Invalid JSON input")

        try:
            payload: dict[str, str|int] = raw_payload
            
            p = int(payload["p"])
            # p_certificate = str(payload.get("p_certificate", ""))
            alpha = int(payload["alpha"])
            a = int(payload["a"])
            k = int(payload["k"])
            message = payload["message"]
            inputType = payload["inputType"]

        except KeyError:
            raise ValueError("Missing required field")

        if inputType == "text":
            m = str2int(str(message))
        else:
            m = int(message)
        
        m = m % p
        
        if k < 0 or k >= p:
            raise ValueError("Invalid k - it must be in the range [0, p)")
        
        # elgamal_check_p_certificate(p, p_certificate)

        one_per_k_mod_p_minus_1 = inverse(k, p - 1)
        if one_per_k_mod_p_minus_1 is None:
            raise ValueError("Invalid k - it must be invertible modulo p-1")

        gamma = modpower(alpha, k, p)
        delta = (m - a * gamma) % (p-1) * one_per_k_mod_p_minus_1 % (p-1)

        return f"{m},{gamma},{delta}"
