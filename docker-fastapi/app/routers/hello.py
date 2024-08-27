from fastapi import APIRouter

router = APIRouter()

@router.get("/hola")
def read_hello():
    return "Hola mundo"
