# src\applications\projects\routers.py

from fastapi import APIRouter, Depends, HTTPException
from sqlmodel.ext.asyncio.session import AsyncSession
from typing import List
from http import HTTPStatus

from src.core.manager_db import get_session
from .controllers import ProjectService
from .schemas import ProjectCreateModel, ProjectResponseModel

project_router = APIRouter(
    prefix="/projects",
    tags=["projects"]
)

@project_router.get("/", response_model=List[ProjectResponseModel])
async def read_projects(session: AsyncSession = Depends(get_session)):
    """Get all projects."""
    projects = await ProjectService(session).get_all_projects()
    return projects

@project_router.post("/", status_code=HTTPStatus.CREATED, response_model=ProjectResponseModel)
async def create_project(
    project_data: ProjectCreateModel, session: AsyncSession = Depends(get_session)
):
    """Create a new project."""
    new_project = await ProjectService(session).create_project(project_data)
    return new_project

@project_router.get("/{project_id}", response_model=ProjectResponseModel, status_code=HTTPStatus.OK)
async def read_project(project_id: int, session: AsyncSession = Depends(get_session)):
    """Get a project by its ID."""
    project = await ProjectService(session).get_project(project_id)
    if not project:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="Project not found")
    return project

@project_router.put("/{project_id}", response_model=ProjectResponseModel, status_code=HTTPStatus.OK)
async def update_project(
    project_id: int,
    update_data: ProjectCreateModel,
    session: AsyncSession = Depends(get_session),
):
    """Update a project."""
    updated_project = await ProjectService(session).update_project(project_id, update_data)
    if not updated_project:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="Project not found")
    return updated_project

@project_router.delete("/{project_id}", status_code=HTTPStatus.NO_CONTENT)
async def delete_project(project_id: int, session: AsyncSession = Depends(get_session)):
    """Delete a project."""
    project = await ProjectService(session).get_project(project_id)
    if not project:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="Project not found")
    await ProjectService(session).delete_project(project_id)
    return {}
