import os
from functools import lru_cache
from typing import Optional

import httpx
from fastapi import Header, HTTPException
from jose import jwt

# Default Keycloak URL used by local development and tests. The port was
# changed from 8080 to 8181 to avoid conflicts with other services.
KEYCLOAK_URL = os.getenv("KEYCLOAK_URL", "http://keycloak:8181")
REALM = os.getenv("KEYCLOAK_REALM", "smartport")
JWKS_URL = f"{KEYCLOAK_URL}/realms/{REALM}/protocol/openid-connect/certs"
ISSUER = f"{KEYCLOAK_URL}/realms/{REALM}"


@lru_cache()
def get_jwks():
    resp = httpx.get(JWKS_URL)
    resp.raise_for_status()
    return resp.json()


def verify_jwt(token: str) -> dict:
    jwks = get_jwks()
    header = jwt.get_unverified_header(token)
    key = next((k for k in jwks["keys"] if k["kid"] == header["kid"]), None)
    if not key:
        raise HTTPException(status_code=401, detail="unknown kid")
    try:
        return jwt.decode(token, key, algorithms=["RS256"], issuer=ISSUER)
    except Exception as exc:  # pragma: no cover - generic exception
        raise HTTPException(status_code=401, detail=str(exc))


async def auth_dependency(
    authorization: Optional[str] = Header(None),
    x_auth_token: Optional[str] = Header(None),
) -> dict:
    token = None
    if authorization and authorization.startswith("Bearer "):
        token = authorization[7:]
    elif x_auth_token:
        token = x_auth_token
    if not token:
        raise HTTPException(status_code=401, detail="missing token")
    return verify_jwt(token)


def get_service_token(client_id: str, client_secret: str) -> str:
    token_url = f"{KEYCLOAK_URL}/realms/{REALM}/protocol/openid-connect/token"
    data = {
        "grant_type": "client_credentials",
        "client_id": client_id,
        "client_secret": client_secret,
    }
    resp = httpx.post(token_url, data=data)
    resp.raise_for_status()
    return resp.json()["access_token"]


def get_password_token(client_id: str, username: str, password: str) -> str:
    token_url = f"{KEYCLOAK_URL}/realms/{REALM}/protocol/openid-connect/token"
    data = {
        "grant_type": "password",
        "client_id": client_id,
        "username": username,
        "password": password,
    }
    resp = httpx.post(token_url, data=data)
    resp.raise_for_status()
    return resp.json()["access_token"]
