import logging

import jwt
from core.config import AUTH_HOST, JWT_ALGORITHM, JWT_PUBLIC_KEY
from fastapi import FastAPI, Request
from httpx import AsyncClient, HTTPError
from py_auth_header_parser import parse_auth_header

logger = logging.getLogger(__name__)


def apply_middleware(app: FastAPI):
    @app.middleware("http")
    async def check_auth(request: Request, call_next):
        headers = request.headers
        auth_header = request.headers.get("Authorization")
        if auth_header is not None:
            username, roles, is_authenticated = parse_header(auth_header)
        else:
            oauth2_service = (
                headers["oauth2_service"] if "oauth2_service" in headers else ""
            )
            auth_url = (
                f"{AUTH_HOST}/api/v1/login/"
                if oauth2_service == ""
                else f"{AUTH_HOST}/api/v1/auth/{oauth2_service}"
            )
            username, roles, is_authenticated = await get_auth_answer(auth_url, headers)
        request.state.username = username
        request.state.roles = roles
        request.state.is_authenticated = is_authenticated
        return await call_next(request)


def parse_header(auth_header):
    parsed_auth_header = parse_auth_header(auth_header)
    jwt_token = parsed_auth_header["access_token"]
    username = None
    roles = None
    try:
        decoded_jwt = jwt.decode(jwt_token, JWT_PUBLIC_KEY, algorithms=[JWT_ALGORITHM])
        username = decoded_jwt["username"]
        roles = decoded_jwt["roles"]
    except (jwt.DecodeError, jwt.ExpiredSignatureError) as jwt_error:
        logger.exception(jwt_error)
    is_authenticated = username and roles
    return username, roles, is_authenticated


async def get_auth_answer(auth_url, headers):
    username = None
    roles = None
    is_authenticated = False
    try:
        async with AsyncClient() as client:
            auth_answer = await client.get(auth_url, headers=dict(headers))
            username, roles, is_authenticated = parse_header(auth_answer.headers)
            logger.info(auth_answer)
    except HTTPError as request_error:
        logger.exception(request_error)
    return username, roles, is_authenticated
