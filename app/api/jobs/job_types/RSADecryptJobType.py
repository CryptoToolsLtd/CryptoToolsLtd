from .JobType import JobType
from typing import override
from crypto import modpower, int2str # type: ignore

class RSADecryptJobType(JobType):
    @override
    def __init__(self):
        super().__init__(job_type="RSADecrypt", immediate=True)
    
    @override
    def __call__(self, input: str) -> str:
        c, d, n = map(int, input.split(','))
        m = modpower(c, d, n)
        text = int2str(m)
        return f"{m},{text}"
