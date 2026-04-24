from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.evaluation import router as evaluation_router
from app.api.health import router as health_router
from app.api.iseo import router as iseo_router
from app.core.db import init_db
from app.core.logging import configure_logging


def create_app() -> FastAPI:
    configure_logging()
    init_db()

    app = FastAPI(title="ISEO v2", version="0.4.0")

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=False,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.include_router(health_router, tags=["health"])
    app.include_router(iseo_router, prefix="/iseo", tags=["iseo"])
    app.include_router(evaluation_router, prefix="/evaluation", tags=["evaluation"])

    try:
        from app.api.rag import router as rag_router

        app.include_router(rag_router, prefix="/rag", tags=["rag"])
    except Exception as exc:
        print(f"RAG router disabled at startup: {exc}")

    return app


app = create_app()
