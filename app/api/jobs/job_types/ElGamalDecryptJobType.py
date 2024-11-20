from .JobType import JobType
from typing import override
from crypto import int2str, modpower, inverse, BitPaddingConfig # type: ignore
import json
from .elgamal_tools import convert_primitive_root_to_plain_number

class ElGamalDecryptJobType(JobType):
    @override
    def __init__(self):
        super().__init__(job_type="ElGamalDecrypt", immediate=True)
    
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
            a = int(payload["a"])
            y1 = int(payload["y1"])
            y2 = int(payload["y2"])
            leftPad = int(payload["leftPad"])
            rightPad = int(payload["rightPad"])

        except KeyError:
            raise ValueError("Missing required field")

        if leftPad < 0 or rightPad < 0:
            raise ValueError("Invalid padding")

        # x = y2 * modpower(y1, p - 1 - a, p) % p
        s = modpower(y1, a, p)
        s = inverse(s, p)
        if s is None:
            raise RuntimeError(f"Could not find s such that y1^a * s = 1 mod p. y1 = {y1}, a = {a}, p = {p}")
        x = y2 * s % p
        m = convert_primitive_root_to_plain_number(
            BitPaddingConfig(LEFT_PADDING_SIZE=leftPad, RIGHT_PADDING_SIZE=rightPad),
            x,
        )
        mText = int2str(m)

        return f"{s},{x},{m},{mText}"
