# src\applications\hyperparameters\controllers.py

from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel import select
from fastapi import HTTPException
from http import HTTPStatus
from .models import Hyperparameter
from .schemas import HyperparameterCreateModel
from src.applications.prompts.models import Prompt
from src.applications.projects.models import Project

class HyperparameterService:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_all_hyperparameters(self):
        """
        Get all hyperparameter sets.
        """
        statement = select(Hyperparameter).order_by(Hyperparameter.hyperparameter_id)
        result = await self.session.exec(statement)
        return result.all()

    async def get_hyperparameters_by_prompt(self, prompt_id: int):
        """
        Get all hyperparameter sets for a specific prompt.
        """
        statement = select(Hyperparameter).where(Hyperparameter.prompt_id == prompt_id).order_by(Hyperparameter.hyperparameter_id)
        result = await self.session.exec(statement)
        return result.all()

    async def create_hyperparameter(self, hyperparameter_data: HyperparameterCreateModel):
        """
        Create a new hyperparameter set.
        """
        # Verify the prompt and project exist
        prompt_statement = select(Prompt).where(Prompt.prompt_id == hyperparameter_data.prompt_id)
        project_statement = select(Project).where(Project.project_id == hyperparameter_data.project_id)

        prompt_result = await self.session.exec(prompt_statement)
        project_result = await self.session.exec(project_statement)

        if not prompt_result.first() or not project_result.first():
            raise HTTPException(
                status_code=HTTPStatus.BAD_REQUEST,
                detail="Prompt or Project with provided ID does not exist."
            )

        new_hyperparameter = Hyperparameter(**hyperparameter_data.model_dump())
        self.session.add(new_hyperparameter)
        await self.session.commit()
        await self.session.refresh(new_hyperparameter)
        return new_hyperparameter

    async def get_hyperparameter(self, hyperparameter_id: int):
        """
        Get a hyperparameter set by its ID.
        """
        statement = select(Hyperparameter).where(Hyperparameter.hyperparameter_id == hyperparameter_id)
        result = await self.session.exec(statement)
        return result.first()

    async def update_hyperparameter(self, hyperparameter_id: int, hyperparameter_data: HyperparameterCreateModel):
        """
        Update an existing hyperparameter set by its ID.
        """
        statement = select(Hyperparameter).where(Hyperparameter.hyperparameter_id == hyperparameter_id)
        result = await self.session.exec(statement)
        hyperparameter = result.first()

        if not hyperparameter:
            raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="Hyperparameter set not found")

        for key, value in hyperparameter_data.model_dump().items():
            setattr(hyperparameter, key, value)

        await self.session.commit()
        await self.session.refresh(hyperparameter)
        return hyperparameter

    async def delete_hyperparameter(self, hyperparameter_id: int):
        """
        Delete a hyperparameter set by its ID.
        """
        statement = select(Hyperparameter).where(Hyperparameter.hyperparameter_id == hyperparameter_id)
        result = await self.session.exec(statement)
        hyperparameter = result.first()

        if not hyperparameter:
            raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="Hyperparameter set not found")

        await self.session.delete(hyperparameter)
        await self.session.commit()
