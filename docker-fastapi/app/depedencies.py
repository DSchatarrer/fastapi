from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter()

@router.get("/hola")
def read_hello():
    return "Hola mucho"

@router.get("/saludo")
def greet_name(name: str):
    return f"Hola, {name}"

class Item(BaseModel):
    message: str
    value: int

@router.get("/json")
def return_json():
    return {
        "message": "Este es un JSON",
        "value": 42
    }
