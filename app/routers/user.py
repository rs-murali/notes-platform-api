from fastapi import APIRouter, Depends, HTTPException
from dependency_injector.wiring import inject, Provide

from app.core.container import Container
from app.services.user_service import UserService
from app.core.models import UserCreate, UserUpdate

router = APIRouter(
    prefix="/users",
    tags=["users"],
    responses={404: {"description": "Not found"}},
)

@router.get("/")
@inject
async def read_users(
    user_service: UserService = Depends(Provide[Container.user_service])
):
    return user_service.get_users()

@router.get("/{user_id}")
@inject
async def read_user(
    user_id: str, 
    user_service: UserService = Depends(Provide[Container.user_service])
):
    user = user_service.get_user(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@router.post("/", status_code=201)
@inject
async def create_user(
    user: UserCreate, 
    user_service: UserService = Depends(Provide[Container.user_service])
):
    return user_service.create_user(user)

@router.put("/{user_id}")
@inject
async def update_user(
    user_id: str, 
    user: UserUpdate, 
    user_service: UserService = Depends(Provide[Container.user_service])
):
    success = user_service.update_user(user_id, user)
    if not success:
        raise HTTPException(status_code=404, detail="User not found")
    return {"status": "updated"}

@router.delete("/{user_id}")
@inject
async def delete_user(
    user_id: str, 
    user_service: UserService = Depends(Provide[Container.user_service])
):
    success = user_service.delete_user(user_id)
    if not success:
        raise HTTPException(status_code=404, detail="User not found")
    return {"status": "deleted"}
