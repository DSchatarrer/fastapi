# src\applications\models\schemas.py

from pydantic import BaseModel
from .models import Model

class ModelResponseModel(Model):
    """
    Validates response for a model.
    """
    pass

class ModelCreateModel(BaseModel):
    """
    Validates data for creating or updating a model.
    """
    project_id: int
    name: str
    version: str

    model_config = {
        "json_schema_extra": {
            "example": {
                "project_id": 1,
                "name": "ML Model",
                "version": "1.0"
            }
        }
    }
