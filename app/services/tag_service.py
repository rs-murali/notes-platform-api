from typing import List
from app.repositories.tags_repo import TagRepository

class TagService:
    def __init__(self, tag_repo: TagRepository):
        self.tag_repo = tag_repo

    def get_or_create_tags(self, user_id: str, tag_names: List[str]) -> List[str]:
        tag_ids = []
        for name in tag_names:
            tag_id = self.tag_repo.get_tag_by_name(user_id, name)
            if not tag_id:
                tag_id = self.tag_repo.create_tag(user_id, name)
            tag_ids.append(tag_id)
        return tag_ids

    def link_tags_to_note(self, note_id: str, tag_ids: List[str]) -> None:
        self.tag_repo.link_tags_to_note(note_id, tag_ids)

    def get_tags(self, user_id: str) -> List[dict]:
        return self.tag_repo.list_tags(user_id)
