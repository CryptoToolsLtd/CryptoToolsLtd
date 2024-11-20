from .JobType import JobType
from typing import override
from crypto import str2int, modpower, inverse, BitPaddingConfig # type: ignore
import json
from .elgamal_tools import elgamal_check_p_certificate, convert_plain_number_to_primitive_root

class ElGamalEncryptJobType(JobType):
    @override
    def __init__(self):
        super().__init__(job_type="ElGamalEncrypt", immediate=True)
    
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
            p_certificate = str(payload.get("p_certificate", ""))
            alpha = int(payload["alpha"])
            beta = int(payload["beta"])
            k = int(payload["k"])
            message = payload["message"]
            inputType = payload["inputType"]
            leftPad = int(payload["leftPad"])
            rightPad = int(payload["rightPad"])

        except KeyError:
            raise ValueError("Missing required field")

        if leftPad < 0 or rightPad < 0:
            raise ValueError("Invalid padding")

        if inputType == "text":
            m = str2int(str(message))
        else:
            m = int(message)
        
        if m < 0 or m >= p:
            raise ValueError("Message must be in the range [0, p). IF THE MESSAGE IS TOO LONG (BIG), consider using a larger prime number p.")
        
        if k < 0 or k >= p:
            raise ValueError("Invalid k - it must be in the range [0, p)")
        
        fact_of_p_minus_1 = elgamal_check_p_certificate(p, p_certificate)

        x = convert_plain_number_to_primitive_root(
            BitPaddingConfig(LEFT_PADDING_SIZE=leftPad, RIGHT_PADDING_SIZE=rightPad),
            p,
            m,
            fact_of_p_minus_1,
        )

        one_per_x = inverse(x, p)
        if one_per_x is None:
            raise ValueError(f"x is not invertible in Z_p (this should not happen). x = {x}, p = {p}")

        y1 = modpower(alpha, k, p)
        y2 = x * modpower(beta, k, p) % p

        return f"{m},{x},{y1},{y2}"
