from fastapi import FastAPI
import uvicorn

from app.core.container import Container
from app.routers import user, note, tag

def create_app() -> FastAPI:
    # Initialize DI container
    container = Container()
    container.init_resources()

    app = FastAPI(title="Notes API")

    # Attach container to app
    app.container = container

    # Wire dependency-injector modules
    container.wire(
        modules=[
            "app.routers.user",
            "app.routers.note",
            "app.routers.tag",
            "app.services.user_service",
            "app.services.note_service",
            "app.services.tag_service",
        ]
    )
    
    app.include_router(user.router)
    app.include_router(note.router)
    app.include_router(tag.router)

    return app


app = create_app()

if __name__ == "__main__":
    uvicorn.run(
        "app.main:app",   
        host="0.0.0.0",
        port=8000,
        reload=True,
    )
