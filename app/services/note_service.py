from typing import List, Optional
from app.repositories.note_repo import NoteRepository
from app.services.tag_service import TagService
from app.core.models import NoteCreate, NoteUpdate

class NoteService:
    def __init__(self, note_repo: NoteRepository, tag_service: TagService):
        self.note_repo = note_repo
        self.tag_service = tag_service

    def get_notes(
        self,
        user_id: str,
        status: Optional[str] = None,
        tag: Optional[str] = None,
        search: Optional[str] = None,
        limit: int = 20,
        offset: int = 0,
    ) -> List[dict]:
        return self.note_repo.list_notes(
            user_id=user_id,
            status=status,
            tag=tag,
            search=search,
            limit=limit,
            offset=offset,
        )

    def get_note(self, note_id: str, user_id: str) -> Optional[dict]:
        return self.note_repo.get_note_by_id(note_id, user_id)

    def create_note(self, user_id: str, note_data: NoteCreate) -> str:
        # Create the note
        note_id = self.note_repo.create_note(
            user_id=user_id,
            title=note_data.title,
            content=note_data.content,
            status=note_data.status
        )
        
        # Handle tags
        if note_data.tags:
            tag_ids = self.tag_service.get_or_create_tags(user_id, note_data.tags)
            self.tag_service.link_tags_to_note(note_id, tag_ids)
            
        return note_id

    def update_note(self, note_id: str, user_id: str, note_data: NoteUpdate) -> None:
        self.note_repo.update_note(
            note_id=note_id,
            user_id=user_id,
            title=note_data.title,
            content=note_data.content,
            status=note_data.status
        )
        
        # Handle tags if provided
        if note_data.tags is not None:
            tag_ids = self.tag_service.get_or_create_tags(user_id, note_data.tags)
            self.tag_service.link_tags_to_note(note_id, tag_ids)

    def delete_note(self, note_id: str, user_id: str) -> None:
        return self.note_repo.delete_note(note_id, user_id)
