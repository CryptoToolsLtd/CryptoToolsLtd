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

#############################################
# Environment variables should be consumed by
# importing the following variables, not by
# reading os.environ directly.
#############################################

FLASK_ENV = readNonEmptyStringEnv("FLASK_ENV")

SECRET_KEY = readNonEmptyStringEnv("SECRET_KEY")

MYSQL_HOSTNAME = readUriComponentEnv("MYSQL_HOSTNAME")
MYSQL_HOSTPORT = readUriComponentEnv("MYSQL_HOSTPORT")
MYSQL_USERNAME = readUriComponentEnv("MYSQL_USERNAME")
MYSQL_PASSWORD = readUriComponentEnv("MYSQL_PASSWORD")
MYSQL_DATABASE = readUriComponentEnv("MYSQL_DATABASE")
