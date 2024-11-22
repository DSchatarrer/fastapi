# src\applications\prompts\controllers.py

from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel import select
from fastapi import HTTPException
from http import HTTPStatus

from .models import Prompt
from .schemas import PromptCreateModel
from src.applications.models.models import Model
from src.applications.projects.models import Project
from src.applications.hyperparameters.models import Hyperparameter

class PromptService:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_all_prompts(self):
        """
        Get all prompts.
        """
        statement = select(Prompt).order_by(Prompt.prompt_id)
        result = await self.session.exec(statement)
        return result.all()

    async def get_prompts_by_project(self, project_id: int):
        """
        Get all prompts for a specific project.
        """
        statement = select(Prompt).where(Prompt.project_id == project_id).order_by(Prompt.prompt_id)
        result = await self.session.exec(statement)
        return result.all()

    async def get_prompts_by_model(self, model_id: int):
        """
        Get all prompts for a specific model.

        Args:
            model_id (int): The ID of the model.

        Returns:
            List[Prompt]: A list of prompts associated with the model.
        """
        statement = select(Prompt).where(Prompt.model_id == model_id).order_by(Prompt.prompt_id)
        result = await self.session.exec(statement)
        return result.all()

    async def create_prompt(self, prompt_data: PromptCreateModel):
        """
        Create a new prompt.
        """
        # Verify the model and project exist
        model_statement = select(Model).where(Model.model_id == prompt_data.model_id)
        project_statement = select(Project).where(Project.project_id == prompt_data.project_id)

        model_result = await self.session.exec(model_statement)
        project_result = await self.session.exec(project_statement)

        if not model_result.first() or not project_result.first():
            raise HTTPException(
                status_code=HTTPStatus.BAD_REQUEST,
                detail="Model or Project with provided ID does not exist."
            )

        # Verify that a prompt with the same name doesn't exist in the given project and model
        prompt_statement = select(Prompt).where(
            Prompt.name == prompt_data.name,
            Prompt.project_id == prompt_data.project_id,
            Prompt.model_id == prompt_data.model_id
        )
        existing_prompt = await self.session.exec(prompt_statement)

        if existing_prompt.first():
            raise HTTPException(
                status_code=HTTPStatus.CONFLICT,
                detail=f"A prompt with the name '{prompt_data.name}' already exists for the specified project and model."
            )

        # Create the new prompt
        new_prompt = Prompt(**prompt_data.model_dump())
        self.session.add(new_prompt)
        await self.session.commit()
        await self.session.refresh(new_prompt)
        return new_prompt

    async def get_prompt(self, prompt_id: int):
        """
        Get a prompt by its ID.
        """
        statement = select(Prompt).where(Prompt.prompt_id == prompt_id)
        result = await self.session.exec(statement)
        return result.first()

    async def update_prompt(self, prompt_id: int, prompt_data: PromptCreateModel):
        """
        Update an existing prompt by its ID.
        """
        # Check if the prompt exists
        statement = select(Prompt).where(Prompt.prompt_id == prompt_id)
        result = await self.session.exec(statement)
        prompt = result.first()

        if not prompt:
            raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="Prompt not found")

        # Validate if the new model_id exists
        model_statement = select(Model).where(Model.model_id == prompt_data.model_id)
        model_result = await self.session.exec(model_statement)
        if not model_result.first():
            raise HTTPException(
                status_code=HTTPStatus.BAD_REQUEST,
                detail=f"Model with ID {prompt_data.model_id} does not exist."
            )

        # Validate if the new project_id exists
        project_statement = select(Project).where(Project.project_id == prompt_data.project_id)
        project_result = await self.session.exec(project_statement)
        if not project_result.first():
            raise HTTPException(
                status_code=HTTPStatus.BAD_REQUEST,
                detail=f"Project with ID {prompt_data.project_id} does not exist."
            )

        # Update fields
        for key, value in prompt_data.model_dump().items():
            setattr(prompt, key, value)

        await self.session.commit()
        await self.session.refresh(prompt)
        return prompt

    async def delete_prompt(self, prompt_id: int):
        """
        Delete a prompt by its ID.
        """
        statement = select(Prompt).where(Prompt.prompt_id == prompt_id)
        result = await self.session.exec(statement)
        prompt = result.first()

        if not prompt:
            raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="Prompt not found")

        await self.session.delete(prompt)
        await self.session.commit()
        

    async def fetch_prompt(self, prompt_id: int):
        """
        Fetch detailed information about a prompt, its hyperparameters, and the associated model.

        Args:
            prompt_id (int): The ID of the prompt to fetch.

        Returns:
            list[dict]: A JSON with details of the prompt, hyperparameters, and model.
        """
        # Fetch the prompt
        prompt_statement = select(Prompt).where(Prompt.prompt_id == prompt_id)
        prompt_result = await self.session.exec(prompt_statement)
        prompt = prompt_result.first()

        if not prompt:
            raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="Prompt not found")

        # Fetch the hyperparameters associated with the prompt
        hyperparameter_statement = select(Hyperparameter).where(Hyperparameter.prompt_id == prompt_id)
        hyperparameter_result = await self.session.exec(hyperparameter_statement)
        hyperparameters = hyperparameter_result.first()

        if not hyperparameters:
            raise HTTPException(
                status_code=HTTPStatus.NOT_FOUND,
                detail="No hyperparameters found for the given prompt"
            )

        # Fetch the model associated with the prompt
        model_statement = select(Model).where(Model.model_id == prompt.model_id)
        model_result = await self.session.exec(model_statement)
        model = model_result.first()

        if not model:
            raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="Model not found for the given prompt")

        # Prepare the response
        response_data = [
            {
                "prompt": {
                    "prompt_text": prompt.prompt_text,
                    "description": prompt.description,
                    "prompt_name": prompt.name
                },
                "hyperparameters": {
                    "hyperparameter_name": hyperparameters.name,
                    "hyperparameter_description": hyperparameters.description,
                    "top_k": hyperparameters.top_k,
                    "top_p": hyperparameters.top_p,
                    "temperature": hyperparameters.temperature,
                    "max_tokens": hyperparameters.max_tokens,
                    "seed": hyperparameters.seed
                },
                "model": {
                    "model_name": model.name,
                    "model_version": model.version
                }
            }
        ]

        return response_data
