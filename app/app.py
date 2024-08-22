from fastapi import FastAPI, APIRouter, Request, HTTPException, UploadFile, Depends, Body, File
from fastapi_socketio import SocketManager
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from uuid import UUID
import time
import os
import pandas as pd
from datetime import datetime
from fastapi.middleware.cors import CORSMiddleware

from app.config import get_settings, Settings

def create_app():
    # Configuraciones iniciales
    app = FastAPI()
    socket_manager = SocketManager(app=app)

    # Middleware de CORS
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],  # Ajusta esto según tus necesidades
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Variables de entorno
    UPLOAD_FOLDER = os.environ.get("UPLOAD_FOLDER", "./uploads")
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)

    # Definiciones de modelos de entrada
    class Message(BaseModel):
        sessionKey: UUID
        pregunta: str

    class ProgressStateManager:
        def __init__(self):
            self._progress_states = {}

        def get_state(self, session_key):
            return self._progress_states.get(session_key, {"step": "0", "descripcion": "Inicializando"})

        def update(self, session_key, step, descripcion):
            self._progress_states[session_key] = {"step": step, "descripcion": descripcion}
            socket_manager.emit('progress_update', {'sessionKey': session_key, 'step': step, 'descripcion': descripcion}, room=session_key)

        def reset(self, session_key):
            self._progress_states[session_key] = {"step": "0", "descripcion": "Inicializando"}

    progress_manager = ProgressStateManager()

    # Routers
    api_router = APIRouter()

    @api_router.post("/api/send-message")
    async def api_ai(data: dict = Body(...), settings: Settings = Depends(get_settings)):
        # Capturar el body y devolverlo directamente
        return JSONResponse(content=data)

    @api_router.get("/api/progress")
    async def get_progress(sessionKey: UUID, settings: Settings = Depends(get_settings)):
        return JSONResponse(content=progress_manager.get_state(sessionKey))

    @api_router.post("/api/upload-files")
    async def upload_files(
        files: list[UploadFile] = File(...), 
        settings: Settings = Depends(get_settings)
    ):
        if not files:
            raise HTTPException(status_code=400, detail="No se proporcionaron archivos")

        saved_files = []
        for file in files:
            file_path = os.path.join(UPLOAD_FOLDER, file.filename)
            with open(file_path, "wb") as f:
                f.write(await file.read())  # Leer y guardar el contenido del archivo
            saved_files.append(file.filename)

        return JSONResponse(content={"message": "Archivos subidos exitosamente", "files": saved_files})

    @socket_manager.on('connect')
    async def handle_connect(sid, environ):
        session_key = environ.get('HTTP_SESSIONKEY')
        if session_key:
            socket_manager.enter_room(sid, session_key)
            await socket_manager.emit('connected', {'message': f'Connected to session {session_key}'}, room=session_key)

    @socket_manager.on('disconnect')
    async def handle_disconnect(sid):
        session_key = socket_manager.get_sid_room(sid)
        if session_key:
            socket_manager.leave_room(sid, session_key)

    # Inicializar rutas y aplicación
    app.include_router(api_router)

    return app

app = create_app()

# uvicorn app.app:app --host 0.0.0.0 --port 8000 --reload
