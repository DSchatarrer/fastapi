# backend\src\main.py

import uvicorn
import logging
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

try:
    from src.core.settings import settings
    from src.core.manager_db_sync import init_db
except ImportError:
    from core.settings import settings
    from core.manager_db_sync import init_db


def create_app() -> FastAPI: 

    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)

    logging.getLogger('sqlalchemy.engine').setLevel(logging.WARNING)
    logging.getLogger('msal').setLevel(logging.WARNING)
    logging.getLogger('urllib3').setLevel(logging.WARNING)
    logging.getLogger("httpx").setLevel(logging.WARNING)
    logging.getLogger("httpcore").setLevel(logging.WARNING)
    logging.getLogger("botocore").setLevel(logging.WARNING)
    logging.getLogger("boto3").setLevel(logging.WARNING)
    logging.getLogger("s3transfer").setLevel(logging.WARNING)

    @asynccontextmanager
    async def lifespan(app: FastAPI):
        logger.info("server is starting")
        init_db()
        yield 
        logger.info("server is shuttting down")

    app = FastAPI(
        title="Nutricion service",
        version="0.1.0",
        description="A simple web service for a nutricion",
        openapi_url="/openapi.json",
        docs_url="/docs",
        root_path="/nutricion",
        lifespan=lifespan
    )

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.state.logger = logger

    try:
        from src.applications.pacientes.router import paciente_router
        from src.applications.login.router import login_router
    except ImportError:
        from applications.pacientes.router import paciente_router
        from applications.login.router import login_router
        
    app.include_router(login_router)
    app.include_router(paciente_router)


    return app

app = create_app()


if __name__ == "__main__":
    uvicorn.run(app, 
                host=settings.FASTAPI_RUN_HOST, 
                port=settings.FASTAPI_RUN_PORT)

