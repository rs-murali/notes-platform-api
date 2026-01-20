"""
Dependency injector container for the application.
"""
from dependency_injector import containers, providers
from app.core import AppConfig
from app.db import PostgresPool

class Container(containers.DeclarativeContainer):

    config = providers.Singleton(AppConfig)
    
    postgres_pool = providers.Singleton(
        PostgresPool,
        dsn=config.provided.postgres_url,
        minconn=1,
        maxconn=10,
    )
