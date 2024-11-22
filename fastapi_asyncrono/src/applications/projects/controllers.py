# src\applications\projects\controllers.py

from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel import select
from .models import Project
from .schemas import ProjectCreateModel
from fastapi import HTTPException
from http import HTTPStatus

class ProjectService:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_all_projects(self):
        """
        Get all projects.
        """
        statement = select(Project).order_by(Project.project_id)
        result = await self.session.exec(statement)
        return result.all()

    async def create_project(self, project_data: ProjectCreateModel):
        """
        Create a new project.
        """
        # Check if a project with the same name already exists
        statement = select(Project).where(Project.name == project_data.name)
        result = await self.session.exec(statement)
        existing_project = result.first()

        if existing_project:
            raise HTTPException(
                status_code=HTTPStatus.CONFLICT,
                detail="A project with this name already exists."
            )

        new_project = Project(**project_data.model_dump())
        self.session.add(new_project)
        await self.session.commit()
        await self.session.refresh(new_project)
        return new_project

    async def get_project(self, project_id: int):
        """
        Get a project by its ID.
        """
        statement = select(Project).where(Project.project_id == project_id)
        result = await self.session.exec(statement)
        return result.first()

    async def update_project(self, project_id: int, project_data: ProjectCreateModel):
        """
        Update an existing project by its ID.
        """
        # Ensure no other project has the same name
        statement = select(Project).where(
            Project.name == project_data.name, Project.project_id != project_id
        )
        result = await self.session.exec(statement)
        conflicting_project = result.first()

        if conflicting_project:
            raise HTTPException(
                status_code=HTTPStatus.CONFLICT,
                detail="Another project with this name already exists."
            )

        statement = select(Project).where(Project.project_id == project_id)
        result = await self.session.exec(statement)
        project = result.first()

        if not project:
            return None

        for key, value in project_data.model_dump().items():
            setattr(project, key, value)

        await self.session.commit()
        await self.session.refresh(project)
        return project

    async def delete_project(self, project_id: int):
        """
        Delete a project by its ID.
        """
        statement = select(Project).where(Project.project_id == project_id)
        result = await self.session.exec(statement)
        project = result.first()

        if not project:
            return None

        await self.session.delete(project)
        await self.session.commit()
