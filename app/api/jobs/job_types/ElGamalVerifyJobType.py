from .JobType import JobType
from typing import override
from crypto import modpower # type: ignore
import json

class ElGamalVerifyJobType(JobType):
    @override
    def __init__(self):
        super().__init__(job_type="ElGamalVerify", immediate=True)
    
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
            beta = int(payload["beta"])
            gamma = int(payload["gamma"]) % p
            delta = int(payload["delta"]) % (p-1)
            m = int(payload["m"]) % p

        except KeyError:
            raise ValueError("Missing required field")
        
        v1 = modpower(beta, gamma, p) * modpower(gamma, delta, p) % p
        v2 = modpower(alpha, m, p)
        isEqual = "true" if v1 == v2 else "false"

        return f"{v1},{v2},{isEqual}"
