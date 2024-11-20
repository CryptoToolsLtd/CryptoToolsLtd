from .JobType import JobType
from typing import override
from crypto import modpower, str2int # type: ignore
import json
import re

class RSAEncryptJobType(JobType):
    @override
    def __init__(self):
        super().__init__(job_type="RSAEncrypt", immediate=True)
    
    @override
    def __call__(self, input: str) -> str:
        payload = json.loads(input)
        if not isinstance(payload, dict):
            raise ValueError("Input must be a JSON object")

        try:
            e = int(payload['e']) # type: ignore
            n = int(payload['n']) # type: ignore
            message = payload['message'] # type: ignore
            if payload['inputType'] == 'number':
                m = int(message) # type: ignore
            else:
                text = message # type: ignore
                if not isinstance(text, str):
                    raise ValueError("Message must be a string")
                if not re.match(r'^[a-zA-Z]+$', text):
                    raise ValueError("Message must only contain alpha characters")
                m = str2int(text)
        except KeyError as e:
            raise ValueError(f"Missing key: {e}")
        
        c = modpower(m, e, n)
        return f"{m},{c}"
