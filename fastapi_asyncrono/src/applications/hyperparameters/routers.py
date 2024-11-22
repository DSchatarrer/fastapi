# src\applications\hyperparameters\routers.py

from fastapi import APIRouter, Depends, HTTPException
from sqlmodel.ext.asyncio.session import AsyncSession
from typing import List
from src.core.manager_db import get_session
from http import HTTPStatus
from .controllers import HyperparameterService
from .schemas import HyperparameterCreateModel, HyperparameterResponseModel

hyperparameter_router = APIRouter(
    prefix="/hyperparameters",
    tags=["hyperparameters"]
)

@hyperparameter_router.get("/", response_model=List[HyperparameterResponseModel])
async def read_hyperparameters(session: AsyncSession = Depends(get_session)):
    """Get all hyperparameter sets."""
    hyperparameters = await HyperparameterService(session).get_all_hyperparameters()
    return hyperparameters

@hyperparameter_router.get("/prompt/{prompt_id}", response_model=List[HyperparameterResponseModel], status_code=HTTPStatus.OK)
async def read_hyperparameters_by_prompt(prompt_id: int, session: AsyncSession = Depends(get_session)):
    """Get all hyperparameter sets for a specific prompt."""
    hyperparameters = await HyperparameterService(session).get_hyperparameters_by_prompt(prompt_id)
    return hyperparameters

@hyperparameter_router.post("/", status_code=HTTPStatus.CREATED, response_model=HyperparameterResponseModel)
async def create_hyperparameter(
    hyperparameter_data: HyperparameterCreateModel, session: AsyncSession = Depends(get_session)
):
    """Create a new hyperparameter set."""
    new_hyperparameter = await HyperparameterService(session).create_hyperparameter(hyperparameter_data)
    return new_hyperparameter

@hyperparameter_router.get("/{hyperparameter_id}", response_model=HyperparameterResponseModel, status_code=HTTPStatus.OK)
async def read_hyperparameter(hyperparameter_id: int, session: AsyncSession = Depends(get_session)):
    """Get a hyperparameter set by its ID."""
    hyperparameter = await HyperparameterService(session).get_hyperparameter(hyperparameter_id)
    if not hyperparameter:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="Hyperparameter set not found")
    return hyperparameter

@hyperparameter_router.put("/{hyperparameter_id}", response_model=HyperparameterResponseModel, status_code=HTTPStatus.OK)
async def update_hyperparameter(
    hyperparameter_id: int,
    update_data: HyperparameterCreateModel,
    session: AsyncSession = Depends(get_session),
):
    """Update a hyperparameter set."""
    updated_hyperparameter = await HyperparameterService(session).update_hyperparameter(hyperparameter_id, update_data)
    return updated_hyperparameter

@hyperparameter_router.delete("/{hyperparameter_id}", status_code=HTTPStatus.NO_CONTENT)
async def delete_hyperparameter(hyperparameter_id: int, session: AsyncSession = Depends(get_session)):
    """Delete a hyperparameter set."""
    await HyperparameterService(session).delete_hyperparameter(hyperparameter_id)
    return {}
