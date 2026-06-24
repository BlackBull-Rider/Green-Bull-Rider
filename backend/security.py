from fastapi import Header, HTTPException

from backend.services.auth_service import (
    decode_token
)


def get_current_user(
    authorization: str = Header(None)
):

    if not authorization:

        raise HTTPException(
            status_code=401,
            detail="Login Required"
        )

    token = authorization.replace(
        "Bearer ",
        ""
    )

    payload = decode_token(token)

    if not payload:

        raise HTTPException(
            status_code=401,
            detail="Invalid Token"
        )

    return payload


def get_admin_user(
    authorization: str = Header(None)
):

    user = get_current_user(
        authorization
    )

    if user["role"] != "admin":

        raise HTTPException(
            status_code=403,
            detail="Admin Only"
        )

    return user
