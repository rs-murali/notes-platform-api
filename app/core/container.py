"""
Dependency injector container for the application.
"""
from dependency_injector import containers, providers
from app.core.config import AppConfig
from app.db.postgres import PostgresPool
from app.repositories.user_repo import UserRepository
from app.repositories.note_repo import NoteRepository
from app.repositories.tags_repo import TagRepository
from app.services.user_service import UserService
from app.services.note_service import NoteService
from app.services.tag_service import TagService

class Container(containers.DeclarativeContainer):

    config = providers.Singleton(AppConfig)
    
    postgres_pool = providers.Singleton(
        PostgresPool,
        dsn=config.provided.postgres_url,
        minconn=1,
        maxconn=10,
    )

    user_repo = providers.Singleton(
        UserRepository,
        db=postgres_pool,
    )

    note_repo = providers.Singleton(
        NoteRepository,
        db=postgres_pool,
    )

    tag_repo = providers.Singleton(
        TagRepository,
        db=postgres_pool,
    )

    user_service = providers.Factory(
        UserService,
        user_repo=user_repo,
    )

    tag_service = providers.Factory(
        TagService,
        tag_repo=tag_repo,
    )

    note_service = providers.Factory(
        NoteService,
        note_repo=note_repo,
        tag_service=tag_service,
    )
