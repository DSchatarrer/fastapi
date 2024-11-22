# src\applications\models\routers.py

from fastapi import APIRouter, Depends, HTTPException
from sqlmodel.ext.asyncio.session import AsyncSession
from typing import List
from src.core.manager_db import get_session
from http import HTTPStatus
from .controllers import ModelService
from .schemas import ModelCreateModel, ModelResponseModel

model_router = APIRouter(
    prefix="/models",
    tags=["models"]
)

@model_router.get("/", response_model=List[ModelResponseModel])
async def read_models(session: AsyncSession = Depends(get_session)):
    """Get all models."""
    models = await ModelService(session).get_all_models()
    return models

@model_router.get("/project/{project_id}", response_model=List[ModelResponseModel], status_code=HTTPStatus.OK)
async def read_models_by_project(project_id: int, session: AsyncSession = Depends(get_session)):
    """Get all models for a specific project."""
    models = await ModelService(session).get_models_by_project(project_id)
    return models

@model_router.post("/", status_code=HTTPStatus.CREATED, response_model=ModelResponseModel)
async def create_model(
    model_data: ModelCreateModel, session: AsyncSession = Depends(get_session)
):
    """Create a new model."""
    new_model = await ModelService(session).create_model(model_data)
    return new_model

@model_router.get("/{model_id}", response_model=ModelResponseModel, status_code=HTTPStatus.OK)
async def read_model(model_id: int, session: AsyncSession = Depends(get_session)):
    """Get a model by its ID."""
    model = await ModelService(session).get_model(model_id)
    if not model:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="Model not found")
    return model

@model_router.put("/{model_id}", response_model=ModelResponseModel, status_code=HTTPStatus.OK)
async def update_model(
    model_id: int,
    update_data: ModelCreateModel,
    session: AsyncSession = Depends(get_session),
):
    """Update a model."""
    updated_model = await ModelService(session).update_model(model_id, update_data)
    return updated_model

@model_router.delete("/{model_id}", status_code=HTTPStatus.NO_CONTENT)
async def delete_model(model_id: int, session: AsyncSession = Depends(get_session)):
    """Delete a model."""
    await ModelService(session).delete_model(model_id)
    return {}
