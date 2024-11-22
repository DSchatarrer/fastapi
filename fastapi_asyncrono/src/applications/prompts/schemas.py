# src\applications\prompts\schemas.py

from pydantic import BaseModel
from .models import Prompt

class PromptResponseModel(Prompt):
    """
    Validates response for a prompt.
    """
    pass

class PromptCreateModel(BaseModel):
    """
    Validates data for creating or updating a prompt.
    """
    model_id: int
    project_id: int
    name: str
    description: str | None = None
    prompt_text: str

    model_config = {
        "json_schema_extra": {
            "example": {
                "model_id": 1,
                "project_id": 1,
                "name": "Sample Prompt",
                "description": "This is a sample prompt.",
                "prompt_text": "Generate a story based on this prompt."
            }
        }
    }
