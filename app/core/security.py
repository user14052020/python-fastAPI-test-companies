import os
from fastapi import Security, HTTPException
from fastapi.security.api_key import APIKeyHeader
from starlette.status import HTTP_403_FORBIDDEN

API_KEY_NAME = "X-API-Key"
api_key_scheme = APIKeyHeader(name=API_KEY_NAME, auto_error=False)

def api_key_auth(api_key: str = Security(api_key_scheme)) -> str:
    expected = os.getenv("API_KEY", "SECRET_API_KEY")
    if api_key == expected:
        return api_key
    raise HTTPException(status_code=HTTP_403_FORBIDDEN, detail="Invalid API Key")