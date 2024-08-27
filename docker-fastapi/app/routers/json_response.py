from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter()

class Item(BaseModel):
    message: str
    value: int

@router.get("/json")
def return_json():
    return {
        "message": "Este es un JSON",
        "value": 42
    }
