from fastapi import APIRouter
from fastapi import Depends

from backend.security import (
    get_admin_user
)

from backend.services.admin_service import (
    get_pending_users,
    approve_user,
    reject_user,
    block_user,
    get_all_users
)

router = APIRouter(
    prefix="/admin",
    tags=["Admin Panel"]
)


@router.get("/requests")
def requests(
    admin=Depends(get_admin_user)
):

    return get_pending_users()


@router.post("/approve/{user_id}")
def approve(
    user_id: int,
    admin=Depends(get_admin_user)
):

    return approve_user(user_id)


@router.post("/reject/{user_id}")
def reject(
    user_id: int,
    admin=Depends(get_admin_user)
):

    return reject_user(user_id)


@router.post("/block/{user_id}")
def block(
    user_id: int,
    admin=Depends(get_admin_user)
):

    return block_user(user_id)


@router.get("/users")
def users(
    admin=Depends(get_admin_user)
):

    return get_all_users()
