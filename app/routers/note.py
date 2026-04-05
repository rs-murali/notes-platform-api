from fastapi import APIRouter, Depends, HTTPException, Query, Header
from typing import List, Optional
from dependency_injector.wiring import inject, Provide

from app.core.container import Container
from app.services.note_service import NoteService
from app.core.models import NoteCreate, NoteUpdate

router = APIRouter(
    prefix="/notes",
    tags=["notes"],
)

@router.get("/")
@inject
async def list_notes(
    status: Optional[str] = None,
    tag: Optional[str] = None,
    search: Optional[str] = None,
    limit: int = 20,
    offset: int = 0,
    x_user_id: str = Header(..., description="User ID for isolation"),
    note_service: NoteService = Depends(Provide[Container.note_service]),
):
    return note_service.get_notes(
        user_id=x_user_id,
        status=status,
        tag=tag,
        search=search,
        limit=limit,
        offset=offset,
    )

@router.get("/{note_id}")
@inject
async def get_note(
    note_id: str,
    x_user_id: str = Header(..., description="User ID for isolation"),
    note_service: NoteService = Depends(Provide[Container.note_service]),
):
    note = note_service.get_note(note_id, x_user_id)
    if not note:
        raise HTTPException(status_code=404, detail="Note not found")
    return note

@router.post("/", status_code=201)
@inject
async def create_note(
    note_data: NoteCreate,
    x_user_id: str = Header(..., description="User ID for isolation"),
    note_service: NoteService = Depends(Provide[Container.note_service]),
):
    return note_service.create_note(x_user_id, note_data)

@router.put("/{note_id}")
@inject
async def update_note(
    note_id: str,
    note_data: NoteUpdate,
    x_user_id: str = Header(..., description="User ID for isolation"),
    note_service: NoteService = Depends(Provide[Container.note_service]),
):
    note_service.update_note(note_id, x_user_id, note_data)
    return {"status": "updated"}

@router.delete("/{note_id}")
@inject
async def delete_note(
    note_id: str,
    x_user_id: str = Header(..., description="User ID for isolation"),
    note_service: NoteService = Depends(Provide[Container.note_service]),
):
    note_service.delete_note(note_id, x_user_id)
    return {"status": "deleted"}
