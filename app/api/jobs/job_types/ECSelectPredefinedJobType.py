from .JobType import JobType
from typing import override
from crypto import special_curves # type: ignore
from random import randrange

class ECSelectPredefinedJobType(JobType):
    @override
    def __init__(self):
        super().__init__(job_type="ECSelectPredefined", immediate=True)
    
    @override
    def __call__(self, input: str) -> str:
        curve_name = input
        desired_curve = None
        for c in special_curves:
            if c.name == curve_name:
                desired_curve = c
                break
        
        if desired_curve is None:
            raise ValueError(f"Curve {curve_name} not found")
        
        p, a, b = desired_curve.p, desired_curve.a, desired_curve.b
        Px, Py = desired_curve.starting_point
        s = randrange(min(4000, max(2, p // 2)), p)

        return f"{p},{a},{b},{Px},{Py},{s}"
