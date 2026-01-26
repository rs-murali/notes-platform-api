from fastapi import FastAPI
import uvicorn

from app.core.container import Container


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
            "app.api.users",
            "app.api.notes",
            "app.services.user_service",
            "app.services.note_service",
        ]
    )

    return app


app = create_app()

if __name__ == "__main__":
    uvicorn.run(
        "app.main:app",   
        host="0.0.0.0",
        port=8000,
        reload=True,
    )
