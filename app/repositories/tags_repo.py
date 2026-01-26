from typing import List
from app.db.postgres import PostgresPool


class TagRepository:
    def __init__(self, db: PostgresPool):
        self.db = db

    def get_tag_by_name(self, user_id: str, name: str) -> str | None:
        conn = self.db.get_conn()
        try:
            with conn.cursor() as cur:
                cur.execute(
                    """
                    SELECT id
                    FROM tags
                    WHERE user_id = %s AND name = %s;
                    """,
                    (user_id, name),
                )
                row = cur.fetchone()
                return row[0] if row else None
        finally:
            self.db.release_conn(conn)

    def create_tag(self, user_id: str, name: str) -> str:
        conn = self.db.get_conn()
        try:
            with conn.cursor() as cur:
                cur.execute(
                    """
                    INSERT INTO tags (user_id, name)
                    VALUES (%s, %s)
                    RETURNING id;
                    """,
                    (user_id, name),
                )
                tag_id = cur.fetchone()[0]
                conn.commit()
                return tag_id
        finally:
            self.db.release_conn(conn)


    def link_tag_to_note(self, note_id: str, tag_id: str) -> None:
        conn = self.db.get_conn()
        try:
            with conn.cursor() as cur:
                cur.execute(
                    """
                    INSERT INTO note_tags (note_id, tag_id)
                    VALUES (%s, %s)
                    ON CONFLICT DO NOTHING;
                    """,
                    (note_id, tag_id),
                )
                conn.commit()
        finally:
            self.db.release_conn(conn)


    def link_tags_to_note(
        self, note_id: str, tag_ids: List[str]
    ) -> None:
        if not tag_ids:
            return

        conn = self.db.get_conn()
        try:
            with conn.cursor() as cur:
                cur.executemany(
                    """
                    INSERT INTO note_tags (note_id, tag_id)
                    VALUES (%s, %s)
                    ON CONFLICT DO NOTHING;
                    """,
                    [(note_id, tag_id) for tag_id in tag_ids],
                )
                conn.commit()
        finally:
            self.db.release_conn(conn)
