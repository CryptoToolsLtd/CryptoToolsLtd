from .JobType import JobType
from .JKLJobType import *
from .ModuloExponentiationJobType import *
from .CheckPrimeJobType import *
from .FactorJobType import *
from .GeneratePrimesJobType import *
from .GCDJobType import *           

job_types: list[JobType] = [
    JKLJobType(),
    ModularExponentiationJobType(),
    CheckPrimeJobType(),
    FactorJobType(),
    GeneratePrimesJobType(),
    GCDJobType(),
]
