from typing import Optional
from psycopg2.extras import RealDictCursor

from app.db import PostgresPool
from app.core import User, UserCreate, UserUpdate


class UserRepository:
    def __init__(self, db: PostgresPool):
        self.db = db
        
    def list_users(self) -> list[User]:
        conn = self.db.get_conn()
        try:
            with conn.cursor(cursor_factory=RealDictCursor) as cur:
                cur.execute(
                    """
                    SELECT id, name, email
                    FROM users;
                    """
                )
                rows = cur.fetchall()
                return [User(**row) for row in rows]

        finally:
            self.db.release_conn(conn)

    def get_user_by_id(self, user_id: int) -> Optional[User]:
        conn = self.db.get_conn()
        try:
            with conn.cursor(cursor_factory=RealDictCursor) as cur:
                cur.execute(
                    """
                    SELECT id, name, email
                    FROM users
                    WHERE id = %s;
                    """,
                    (user_id,),
                )
                row = cur.fetchone()

                if row is None:
                    return None

                return User(**row)

        finally:
            self.db.release_conn(conn)

    def create_user(self, user: UserCreate) -> int:
        conn = self.db.get_conn()
        try:
            with conn.cursor() as cur:
                cur.execute(
                    """
                    INSERT INTO users (name, email)
                    VALUES (%s, %s)
                    RETURNING id;
                    """,
                    (user.name, user.email),
                )
                user_id = cur.fetchone()[0]
                conn.commit()
                return user_id

        except Exception:
            conn.rollback()
            raise

        finally:
            self.db.release_conn(conn)

    def update_user(self, user: UserUpdate) -> bool:
        conn = self.db.get_conn()
        try:
            with conn.cursor() as cur:
                cur.execute(
                    """
                    UPDATE users
                    SET name = %s,
                        email = %s
                    WHERE id = %s;
                    """,
                    (user.name, user.email, user.id),
                )

                updated = cur.rowcount > 0
                conn.commit()
                return updated

        except Exception:
            conn.rollback()
            raise

        finally:
            self.db.release_conn(conn)


    def delete_user(self, user_id: int) -> bool:
        conn = self.db.get_conn()
        try:
            with conn.cursor() as cur:
                cur.execute(
                    """
                    DELETE FROM users
                    WHERE id = %s;
                    """,
                    (user_id,),
                )

                deleted = cur.rowcount > 0
                conn.commit()
                return deleted

        except Exception:
            conn.rollback()
            raise

        finally:
            self.db.release_conn(conn)
