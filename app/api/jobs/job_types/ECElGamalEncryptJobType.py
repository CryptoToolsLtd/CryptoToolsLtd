from .JobType import JobType
from typing import override
import json
from crypto import is_prime, EllipticCurve, BitPaddingConfig, convert_plain_number_to_point_on_curve, str2int # type: ignore

class ECElGamalEncryptJobType(JobType):
    @override
    def __init__(self):
        super().__init__(job_type="ECElGamalEncrypt", immediate=True)
    
    @override
    def __call__(self, input: str) -> str:
        try:
            payload: dict[str, str|int] = json.loads(input)
        except json.JSONDecodeError:
            raise ValueError("Invalid JSON input")
        if not isinstance(payload, dict): # type: ignore
            raise ValueError("Invalid JSON object")
        
        try:
            p = int(payload["p"])
            a = int(payload["a"])
            b = int(payload["b"])
            Px = int(payload["Px"])
            Py = int(payload["Py"])
            Bx = int(payload["Bx"])
            By = int(payload["By"])
            k = int(payload["k"])
            input_type = str(payload["type"])
            value = str(payload["value"])
        except (KeyError, ValueError):
            raise ValueError("Invalid JSON object")
        
        p_is_prime = (is_prime(p) is not False)
        if not p_is_prime:
            raise NotImplementedError("The case that p is not prime is not supported yet")
        ec = EllipticCurve(p, p_is_prime, a, b, (Px, Py))
        
        if input_type == "point":
            Mx, My = map(int, value.split(","))
        elif input_type == "text":
            try:
                leftpad = int(payload["leftpad"])
                rightpad = int(payload["rightpad"])
            except (KeyError, ValueError):
                raise ValueError("Invalid JSON object")
            
            mText = value
            m = str2int(mText)
            Mx, My = convert_plain_number_to_point_on_curve(BitPaddingConfig(
                LEFT_PADDING_SIZE=leftpad,
                RIGHT_PADDING_SIZE=rightpad
            ), ec, m)
        else:
            raise ValueError(f"Invalid input type: {input_type}")
        
        # Encryption
        P = ec.starting_point
        B = (Bx, By)
        M = (Mx, My)

        if not ec.is_point_on_curve(P):
            raise ValueError("P is not on the curve")
        if not ec.is_point_on_curve(B):
            raise ValueError("B is not on the curve")
        if not ec.is_point_on_curve(M):
            raise ValueError("M is not on the curve")

        M1x, M1y = ec.scale_point(k, P)
        M2x, M2y = ec.add_points(M, ec.scale_point(k, B))

        return f"{Mx},{My},{M1x},{M1y},{M2x},{M2y}"
