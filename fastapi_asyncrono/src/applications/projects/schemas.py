# src\applications\projects\schemas.py

from pydantic import BaseModel
from .models import Project

class ProjectResponseModel(Project):
    """
    Validates response for a project.
    """
    pass


class ProjectCreateModel(BaseModel):
    """
    Validates data for creating a project.
    """
    name: str

    model_config = {
        "json_schema_extra": {
            "example": {
                "name": "AI Development Project"
            }
        }
    }


