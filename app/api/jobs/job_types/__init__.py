from .JobType import JobType
from .JKLJobType import *
from .ModuloExponentiationJobType import *
from .CheckPrimeJobType import *
from .FactorJobType import *
from .GeneratePrimesJobType import *
from .GCDJobType import *          

from .RSAGenerateStep1JobType import *
from .RSAStep1To2JobType import *
from .RSAGenerateStep2JobType import *
from .RSAStep2to3JobType import *
from .RSAEncryptJobType import *
from .RSADecryptJobType import *

job_types: list[JobType] = [
    JKLJobType(),
    ModularExponentiationJobType(),
    CheckPrimeJobType(),
    FactorJobType(),
    GeneratePrimesJobType(),
    GCDJobType(),

    RSAGenerateStep1JobType(),
    RSAStep1To2JobType(),
    RSAGenerateStep2JobType(),
    RSAStep2To3JobType(),
    RSAEncryptJobType(),
    RSADecryptJobType(),
]
