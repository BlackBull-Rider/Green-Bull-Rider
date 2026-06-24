from fastapi import APIRouter
from pydantic import BaseModel

from backend.services.auth_service import (
    register_user,
    login_user
)

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)


class RegisterRequest(BaseModel):

    name: str
    email: str
    mobile: str
    password: str


class LoginRequest(BaseModel):

    email: str
    password: str


@router.post("/register")
def register(request: RegisterRequest):

    return register_user(
        request.name,
        request.email,
        request.mobile,
        request.password
    )


@router.post("/login")
def login(request: LoginRequest):

    return login_user(
        request.email,
        request.password
    )
