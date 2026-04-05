from fastapi import APIRouter, Depends, Header
from typing import List
from dependency_injector.wiring import inject, Provide

from app.core.container import Container
from app.services.tag_service import TagService

router = APIRouter(
    prefix="/tags",
    tags=["tags"],
)

@router.get("/")
@inject
async def list_tags(
    x_user_id: str = Header(..., description="User ID for isolation"),
    tag_service: TagService = Depends(Provide[Container.tag_service]),
):
    return tag_service.get_tags(x_user_id)
