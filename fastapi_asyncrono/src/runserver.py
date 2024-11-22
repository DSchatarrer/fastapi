# src\runserver.py

from dotenv import load_dotenv
load_dotenv()

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from contextlib import asynccontextmanager
from src.core.manager_db import init_db

def create_app() -> FastAPI:

    @asynccontextmanager
    async def lifespan(app: FastAPI):
        print("server is starting")
        await init_db()
        yield 
        print("server is shuttting down")

    app = FastAPI(
        title="Buzon service",
        version="0.1.0",
        description="A simple web service for a email clasfication",
        lifespan=lifespan)

    # Middleware CORS
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    from src.applications.projects.routers import project_router
    from src.applications.models.routers import model_router
    from src.applications.prompts.routers import prompt_router
    from src.applications.hyperparameters.routers import hyperparameter_router
    from src.applications.clasificationes.routers import clasificacion_router

    app.include_router(project_router)
    app.include_router(model_router)
    app.include_router(prompt_router)
    app.include_router(hyperparameter_router)
    app.include_router(clasificacion_router)

    return app

app = create_app()

# uvicorn src.runserver:app --host 0.0.0.0 --port 8000 --reload

