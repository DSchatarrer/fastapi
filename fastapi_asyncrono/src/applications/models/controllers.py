# src\applications\models\controllers.py

from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel import select
from fastapi import HTTPException
from http import HTTPStatus

from .schemas import ModelCreateModel
from .models import Model
from src.applications.projects.models import Project

class ModelService:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_all_models(self):
        """
        Get all models.
        """
        statement = select(Model).order_by(Model.model_id)
        result = await self.session.exec(statement)
        return result.all()
    
    async def get_models_by_project(self, project_id: int):
        """
        Get all models for a specific project.
        
        Args:
            project_id (int): The ID of the project.

        Returns:
            List[Model]: A list of models associated with the project.
        """
        statement = select(Model).where(Model.project_id == project_id).order_by(Model.model_id)
        result = await self.session.exec(statement)
        return result.all()

    async def create_model(self, model_data: ModelCreateModel):
        """
        Create a new model.
        """
        # Verify that the project exists
        project_statement = select(Project).where(Project.project_id == model_data.project_id)
        project_result = await self.session.exec(project_statement)
        existing_project = project_result.first()

        if not existing_project:
            raise HTTPException(
                status_code=HTTPStatus.BAD_REQUEST,
                detail=f"Project with ID {model_data.project_id} does not exist."
            )

        # Check if a model with the same name and version exists for the project
        statement = select(Model).where(
            Model.name == model_data.name,
            Model.version == model_data.version,
            Model.project_id == model_data.project_id
        )
        result = await self.session.exec(statement)
        existing_model = result.first()

        if existing_model:
            raise HTTPException(
                status_code=HTTPStatus.CONFLICT,
                detail="A model with this name and version already exists in the project."
            )

        new_model = Model(**model_data.model_dump())
        self.session.add(new_model)
        await self.session.commit()
        await self.session.refresh(new_model)
        return new_model

    async def get_model(self, model_id: int):
        """
        Get a model by its ID.
        """
        statement = select(Model).where(Model.model_id == model_id)
        result = await self.session.exec(statement)
        return result.first()

    async def update_model(self, model_id: int, model_data: ModelCreateModel):
        """
        Update an existing model by its ID.
        """
        statement = select(Model).where(Model.model_id == model_id)
        result = await self.session.exec(statement)
        model = result.first()

        if not model:
            raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="Model not found")

        for key, value in model_data.model_dump().items():
            setattr(model, key, value)

        await self.session.commit()
        await self.session.refresh(model)
        return model

    async def delete_model(self, model_id: int):
        """
        Delete a model by its ID.
        """
        statement = select(Model).where(Model.model_id == model_id)
        result = await self.session.exec(statement)
        model = result.first()

        if not model:
            raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="Model not found")

        await self.session.delete(model)
        await self.session.commit()
