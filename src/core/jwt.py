from datetime import datetime, timedelta
from typing import Any, Dict, Optional

import jwt
from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.handlers.wsgi import WSGIRequest
from django.utils.translation import gettext as _

User = get_user_model()

JWT_ALGORITHM = "HS256"
JWT_AUTH_HEADER = "HTTP_AUTHORIZATION"
JWT_AUTH_HEADER_PREFIX = "JWT"
JWT_ACCESS_TYPE = "access"
JWT_REFRESH_TYPE = "refresh"
JWT_THIRDPARTY_ACCESS_TYPE = "thirdparty"
JWT_REFRESH_TOKEN_COOKIE_NAME = "refreshToken"

PERMISSIONS_FIELD = "permissions"


def jwt_base_payload(exp_delta: timedelta) -> Dict[str, Any]:
    utc_now = datetime.utcnow()
    payload = {"iat": utc_now, "exp": utc_now + exp_delta}
    return payload


def jwt_user_payload(
    user: User,
    token_type: str,
    exp_delta: timedelta,
    additional_payload: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:

    # TODO: adding something to payload
    payload = jwt_base_payload(exp_delta)
    if additional_payload:
        payload.update(additional_payload)
    return payload


def jwt_encode(payload: Dict[str, Any]) -> str:
    tk = jwt.encode(
        payload,
        settings.SECRET_KEY,
        JWT_ALGORITHM,  # type: ignore
    )
    return tk.decode("utf-8") if not isinstance(tk, str) else tk


def jwt_decode(token: str) -> Dict[str, Any]:
    return jwt.decode(
        token,
        settings.SECRET_KEY,  # type: ignore
        algorithms=JWT_ALGORITHM,
    )


def create_token(payload: Dict[str, Any], exp_delta: timedelta) -> str:
    payload.update(jwt_base_payload(exp_delta))
    return jwt_encode(payload)


def create_access_token(
    user: User, additional_payload: Optional[Dict[str, Any]] = None
) -> str:
    if not additional_payload:
        additional_payload = {}
    additional_payload = {**additional_payload}
    payload = jwt_user_payload(
        user, JWT_ACCESS_TYPE, settings.JWT_TTL_ACCESS, additional_payload
    )
    return jwt_encode(payload)


def create_refresh_token(
    user: User, additional_payload: Optional[Dict[str, Any]] = None
) -> str:
    if not additional_payload:
        additional_payload = {}
    additional_payload = {**additional_payload}
    payload = jwt_user_payload(
        user,
        JWT_REFRESH_TYPE,
        settings.JWT_TTL_REFRESH,
        additional_payload,
    )
    return jwt_encode(payload)


def get_token_from_request(request: WSGIRequest) -> Optional[str]:
    auth = request.META.get(JWT_AUTH_HEADER, "").split(maxsplit=1)
    prefix = JWT_AUTH_HEADER_PREFIX

    if len(auth) != 2 or auth[0].upper() != prefix:
        if request.method == "GET" and settings.ACCEPT_JWT_ON_URL_QUERY_PARAM:
            return request.GET.get(prefix, None)
        return None
    return auth[1]


def get_user_from_payload(payload: Dict[str, Any]) -> Optional[User]:
    # TODO: getting user from payload
    return None


def get_user_from_access_token(token: str) -> Optional[User]:
    payload = jwt_decode(token)
    jwt_type = payload.get("type")
    if jwt_type not in [JWT_ACCESS_TYPE, JWT_THIRDPARTY_ACCESS_TYPE]:
        raise jwt.InvalidTokenError(_("%s không hợp lệ") % (_("Mã"),))
    user = get_user_from_payload(payload)
    return user


def get_user_from_refresh_token(token: str) -> Optional[User]:
    payload = jwt_decode(token)
    jwt_type = payload.get("type")
    if jwt_type != JWT_REFRESH_TYPE:
        raise jwt.InvalidTokenError(_("%s không hợp lệ") % (_("Mã"),))
    user = get_user_from_payload(payload)
    return user
