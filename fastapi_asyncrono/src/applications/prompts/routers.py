# src\applications\prompts\routers.py

from fastapi import APIRouter, Depends, HTTPException
from sqlmodel.ext.asyncio.session import AsyncSession
from typing import List
from src.core.manager_db import get_session
from http import HTTPStatus
from .controllers import PromptService
from .schemas import PromptCreateModel, PromptResponseModel

prompt_router = APIRouter(
    prefix="/prompts",
    tags=["prompts"]
)

@prompt_router.get("/", response_model=List[PromptResponseModel])
async def read_prompts(session: AsyncSession = Depends(get_session)):
    """Get all prompts."""
    prompts = await PromptService(session).get_all_prompts()
    return prompts

@prompt_router.get("/project/{project_id}", response_model=List[PromptResponseModel], status_code=HTTPStatus.OK)
async def read_prompts_by_project(project_id: int, session: AsyncSession = Depends(get_session)):
    """Get all prompts for a specific project."""
    prompts = await PromptService(session).get_prompts_by_project(project_id)
    return prompts

@prompt_router.get("/model/{model_id}", response_model=List[PromptResponseModel], status_code=HTTPStatus.OK)
async def read_prompts_by_model(model_id: int, session: AsyncSession = Depends(get_session)):
    """Get all prompts for a specific model."""
    prompts = await PromptService(session).get_prompts_by_model(model_id)
    return prompts

@prompt_router.post("/", status_code=HTTPStatus.CREATED, response_model=PromptResponseModel)
async def create_prompt(
    prompt_data: PromptCreateModel, session: AsyncSession = Depends(get_session)
):
    """Create a new prompt."""
    new_prompt = await PromptService(session).create_prompt(prompt_data)
    return new_prompt

@prompt_router.get("/{prompt_id}", response_model=PromptResponseModel, status_code=HTTPStatus.OK)
async def read_prompt(prompt_id: int, session: AsyncSession = Depends(get_session)):
    """Get a prompt by its ID."""
    prompt = await PromptService(session).get_prompt(prompt_id)
    if not prompt:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="Prompt not found")
    return prompt

@prompt_router.put("/{prompt_id}", response_model=PromptResponseModel, status_code=HTTPStatus.OK)
async def update_prompt(
    prompt_id: int,
    update_data: PromptCreateModel,
    session: AsyncSession = Depends(get_session),
):
    """Update a prompt."""
    updated_prompt = await PromptService(session).update_prompt(prompt_id, update_data)
    return updated_prompt

@prompt_router.delete("/{prompt_id}", status_code=HTTPStatus.NO_CONTENT)
async def delete_prompt(prompt_id: int, session: AsyncSession = Depends(get_session)):
    """Delete a prompt."""
    await PromptService(session).delete_prompt(prompt_id)
    return {}

@prompt_router.get("/fetch/{prompt_id}", status_code=HTTPStatus.OK)
async def fetch_prompt(prompt_id: int, session: AsyncSession = Depends(get_session)):
    """
    Fetch detailed information about a prompt, its hyperparameters, and the associated model.
    """
    prompt_service = PromptService(session)
    return await prompt_service.fetch_prompt(prompt_id)
