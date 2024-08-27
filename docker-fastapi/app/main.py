from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

try:
    from app.routers import hello, greet, json_response
except:
    from routers import hello, greet, json_response

def create_app() -> FastAPI:
    app = FastAPI()

    # Configuración de CORS
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],  # Permite todas las fuentes
        allow_credentials=True,
        allow_methods=["*"],  # Permite todos los métodos (GET, POST, etc.)
        allow_headers=["*"],  # Permite todos los encabezados
    )

    # Incluir las rutas desde los módulos
    app.include_router(hello.router)
    app.include_router(greet.router)
    app.include_router(json_response.router)

    return app


app = create_app()

