from typing import List, Dict, Optional
from app.db.postgres import PostgresPool


class NoteRepository:
    def __init__(self, db: PostgresPool):
        self.db = db


    def list_notes(
        self,
        user_id: str,
        status: Optional[str] = None,
        tag: Optional[str] = None,
        search: Optional[str] = None,
        limit: int = 20,
        offset: int = 0,
    ) -> List[Dict]:
        conn = self.db.get_conn()
        try:
            with conn.cursor() as cur:
                cur.execute(
                    """
                    SELECT
                        n.id,
                        n.title,
                        n.content,
                        COALESCE(
                            array_agg(t.name) FILTER (WHERE t.name IS NOT NULL),
                            '{}'
                        ) AS tags
                    FROM notes n
                    LEFT JOIN note_tags nt ON nt.note_id = n.id
                    LEFT JOIN tags t ON t.id = nt.tag_id
                    WHERE n.user_id = %s
                      AND n.is_deleted = false
                      AND (%s IS NULL OR n.status = %s)
                      AND (
                            %s IS NULL
                            OR t.name = %s
                          )
                      AND (
                            %s IS NULL
                            OR n.title ILIKE %s
                            OR n.content ILIKE %s
                          )
                    GROUP BY n.id, n.title, n.content
                    ORDER BY n.created_at DESC
                    LIMIT %s OFFSET %s;
                    """,
                    (
                        user_id,
                        status, status,
                        tag, tag,
                        search, f"%{search}%", f"%{search}%",
                        limit, offset,
                    ),
                )

                rows = cur.fetchall()
                return [
                    {
                        "id": row[0],
                        "title": row[1],
                        "content": row[2],
                        "tags": row[3],
                    }
                    for row in rows
                ]
        finally:
            self.db.release_conn(conn)

    def get_note_by_id(
        self,
        note_id: str,
        user_id: str,
    ) -> Optional[Dict]:
        conn = self.db.get_conn()
        try:
            with conn.cursor() as cur:
                cur.execute(
                    """
                    SELECT
                        n.id,
                        n.title,
                        n.content,
                        COALESCE(
                            array_agg(t.name) FILTER (WHERE t.name IS NOT NULL),
                            '{}'
                        ) AS tags
                    FROM notes n
                    LEFT JOIN note_tags nt ON nt.note_id = n.id
                    LEFT JOIN tags t ON t.id = nt.tag_id
                    WHERE n.id = %s
                      AND n.user_id = %s
                      AND n.is_deleted = false
                    GROUP BY n.id, n.title, n.content;
                    """,
                    (note_id, user_id),
                )

                row = cur.fetchone()
                if row is None:
                    return None

                return {
                    "id": row[0],
                    "title": row[1],
                    "content": row[2],
                    "tags": row[3],
                }
        finally:
            self.db.release_conn(conn)


    def create_note(
        self,
        user_id: str,
        title: str,
        content: str,
    ) -> str:
        conn = self.db.get_conn()
        try:
            with conn.cursor() as cur:
                cur.execute(
                    """
                    INSERT INTO notes (user_id, title, content)
                    VALUES (%s, %s, %s)
                    RETURNING id;
                    """,
                    (user_id, title, content),
                )
                note_id = cur.fetchone()[0]
                conn.commit()
                return note_id
        finally:
            self.db.release_conn(conn)

    def update_note(
        self,
        note_id: str,
        user_id: str,
        title: str,
        content: str,
    ) -> None:
        conn = self.db.get_conn()
        try:
            with conn.cursor() as cur:
                cur.execute(
                    """
                    UPDATE notes
                    SET title = %s,
                        content = %s,
                        updated_at = now()
                    WHERE id = %s
                      AND user_id = %s
                      AND is_deleted = false;
                    """,
                    (title, content, note_id, user_id),
                )
                conn.commit()
        finally:
            self.db.release_conn(conn)


    def delete_note(
        self,
        note_id: str,
        user_id: str,
    ) -> None:
        conn = self.db.get_conn()
        try:
            with conn.cursor() as cur:
                cur.execute(
                    """
                    UPDATE notes
                    SET is_deleted = true
                    WHERE id = %s
                      AND user_id = %s;
                    """,
                    (note_id, user_id),
                )
                conn.commit()
        finally:
            self.db.release_conn(conn)
