import jwt
import app.env as ENV
from typing import Any

ALGORITHM = "HS256"

def issue_computation_cert(type: str, content: dict[str, str]) -> str:
    return jwt.encode({ # type: ignore
        "type": type,
        "content": content,
    }, ENV.SECRET_KEY, algorithm=ALGORITHM)

def verify_computation_cert(type: str, token: str) -> dict[str, str]:
    payload = jwt.decode(token, ENV.SECRET_KEY, algorithms=[ALGORITHM]) # type: ignore
    if not isinstance(payload, dict):
        raise ValueError("Invalid computation certificate - invalid payload")
    if type != payload['type']:
        raise ValueError("Invalid computation certificate - type mismatch")
    content: Any = payload['content']
    if not isinstance(content, dict):
        raise ValueError("Invalid computation certificate - invalid content")
    for key in content: # type: ignore
        if not isinstance(key, str) or not isinstance(content[key], str):
            raise ValueError("Invalid computation certificate - invalid content")
    
    c: dict[str, str] = content
    return c
