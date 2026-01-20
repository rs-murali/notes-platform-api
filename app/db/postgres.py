from psycopg2.pool import SimpleConnectionPool

class PostgresPool:
    def __init__(self, dsn: str, minconn: int = 1, maxconn: int = 10):
        self.pool = SimpleConnectionPool(
            minconn=minconn,
            maxconn=maxconn,
            dsn=dsn,
        )

    def get_conn(self):
        return self.pool.getconn()

    def release_conn(self, conn):
        self.pool.putconn(conn)

    def close(self):
        self.pool.closeall()
