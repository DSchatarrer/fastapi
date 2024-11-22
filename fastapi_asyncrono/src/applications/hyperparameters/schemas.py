# src\applications\hyperparameters\schemas.py

from pydantic import BaseModel
from .models import Hyperparameter

class HyperparameterResponseModel(Hyperparameter):
    """
    Validates response for a hyperparameter set.
    """
    pass

class HyperparameterCreateModel(BaseModel):
    """
    Validates data for creating or updating a hyperparameter set.
    """
    prompt_id: int
    project_id: int
    name: str
    description: str | None = None
    top_k: int | None = None
    top_p: float | None = None
    temperature: float | None = None
    max_tokens: int | None = None
    seed: int | None = None

    model_config = {
        "json_schema_extra": {
            "example": {
                "prompt_id": 1,
                "project_id": 1,
                "name": "Sample Hyperparameter Set",
                "description": "This set is optimized for quick response.",
                "top_k": 50,
                "top_p": 0.9,
                "temperature": 0.7,
                "max_tokens": 100,
                "seed": 42
            }
        }
    }
