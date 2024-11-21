from .JobType import JobType
from typing import override
from crypto import is_prime, EllipticCurve, BitPaddingConfig, convert_point_on_curve_to_plain_number, int2str # type: ignore

class ECElGamalDecryptJobType(JobType):
    @override
    def __init__(self):
        super().__init__(job_type="ECElGamalDecrypt", immediate=True)
    
    @override
    def __call__(self, input: str) -> str:
        p, a, b, Px, Py, s, M1x, M1y, M2x, M2y, leftpad, rightpad = map(int, input.split(","))

        p_is_prime = (is_prime(p) is not False)
        if not p_is_prime:
            raise NotImplementedError("The case that p is not prime is not supported yet")
        
        ec = EllipticCurve(p, p_is_prime, a, b, (Px, Py))

        M1 = (M1x, M1y)
        M2 = (M2x, M2y)

        P = ec.starting_point
        if not ec.is_point_on_curve(P):
            raise ValueError("P is not on the curve")
        if not ec.is_point_on_curve(M1):
            raise ValueError("M1 is not on the curve")
        if not ec.is_point_on_curve(M2):
            raise ValueError("M2 is not on the curve")

        sM1 = ec.scale_point(s, M1)
        sM1x, sM1y = sM1
        M = ec.add_points(M2, ec.scale_point(-1, sM1))
        Mx, My = M

        if leftpad == 0 and rightpad == 0:
            m = "N/A"
            mText = "N/A"
        else:
            m = convert_point_on_curve_to_plain_number(BitPaddingConfig(
                LEFT_PADDING_SIZE=leftpad,
                RIGHT_PADDING_SIZE=rightpad,
            ), ec, M)
            mText = int2str(m)
        
        return f"{sM1x},{sM1y},{Mx},{My},{m},{mText}"
