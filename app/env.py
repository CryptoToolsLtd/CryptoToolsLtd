from dotenv import load_dotenv
load_dotenv()

import os
from urllib.parse import quote

def readNonEmptyStringEnv(key: str) -> str:
    value = os.environ.get(key, None)
    if value is None or len(value) == 0:
        raise RuntimeError(f"Environment variable {key} is invalid or missing")
    return value

def readUriComponentEnv(key: str) -> str:
    value = readNonEmptyStringEnv(key)
    return quote(value)

def readIntEnv(key: str) -> int:
    value = readNonEmptyStringEnv(key)
    return int(value)

#############################################
# Environment variables should be consumed by
# importing the following variables, not by
# reading os.environ directly.
#############################################

FLASK_ENV = readNonEmptyStringEnv("FLASK_ENV")

SECRET_KEY = readNonEmptyStringEnv("SECRET_KEY")

MYSQL_HOSTNAME = readUriComponentEnv("MYSQL_HOSTNAME")
MYSQL_HOSTPORT = readIntEnv("MYSQL_HOSTPORT")
MYSQL_USERNAME = readNonEmptyStringEnv("MYSQL_USERNAME")
MYSQL_PASSWORD = readNonEmptyStringEnv("MYSQL_PASSWORD")
MYSQL_DATABASE = readNonEmptyStringEnv("MYSQL_DATABASE")

REDIS_HOSTNAME = readUriComponentEnv("REDIS_HOSTNAME")
REDIS_HOSTPORT = readIntEnv("REDIS_HOSTPORT")
