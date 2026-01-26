# routers/user.py
from fastapi import APIRouter, Depends

from app.services.user_service import UserService

router = APIRouter(
    prefix="/users",
    tags=["users"],
    responses={404: {"description": "Not found"}},
)

@router.get("/")
async def read_users(
    user_service=Depends(UserService)
):
    return user_service.get_users()

@router.get("/{user_id}")
async def read_user(user_id: str, user_service=Depends(UserService)):
    return user_service.get_user(user_id)

@router.post("/")
async def create_user(user: dict, user_service=Depends(UserService)):
    return user_service.create_user(user)

@router.put("/{user_id}")
async def update_user(user_id: str, user: dict, user_service=Depends(UserService)):
    return user_service.update_user(user_id, user)

@router.delete("/{user_id}")
async def delete_user(user_id: str, user_service=Depends(UserService)):
    return user_service.delete_user(user_id)
