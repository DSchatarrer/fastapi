from fastapi import APIRouter

router = APIRouter()

@router.get("/saludo")
def greet_name(name: str):
    return f"Hola, {name}"
