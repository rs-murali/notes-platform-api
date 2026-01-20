# app/main.py
from dependency_injector.wiring import inject, Provide

from app.core.container import Container
from app.db.postgres import PostgresPool


@inject
def main(
    postgres_pool: PostgresPool = Provide[Container.postgres_pool],
):
    print("Hello from notes-api!")
    conn = None
    try:
        conn = postgres_pool.get_conn()
        with conn.cursor() as cur:
            cur.execute("SELECT 1;")
            print("Successfully acquired a connection from the pool.")
    finally:
        if conn:
            postgres_pool.release_conn(conn)
            print("Connection released back to the pool.")


if __name__ == "__main__":
    container = Container()
    container.init_resources()
    container.wire(modules=[__name__])

    main()
