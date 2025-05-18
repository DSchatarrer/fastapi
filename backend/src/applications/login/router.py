# backend\src\applications\login\router.py

from fastapi import (APIRouter, Depends, Response, Request, Depends, BackgroundTasks)
from sqlmodel import Session
from fastapi.responses import StreamingResponse
from http import HTTPStatus
from typing import Optional, List, Dict


from core.manager_db_sync import get_session
from .controller import LoginService
from .schemas import (
    LoginRequest,
    LoginResponse,
    UserCreateRequest
)


login_router = APIRouter(
    prefix="/login",
    tags=["login"],
)


@login_router.post("/")
async def login(
    credentials: LoginRequest,
    request: Request,
    response: Response,
    session: Session = Depends(get_session)
):
    return LoginService(session, request.app.state.logger).login(
        response=response,
        username=credentials.usu,
        password=credentials.pwd
    )


@login_router.post("/alta-usuario")
async def create_user(
    user_data: UserCreateRequest,
    request: Request,
    session: Session = Depends(get_session)
):

    return LoginService(session, request.app.state.logger).create_user(
        username=user_data.usu,
        password=user_data.pwd,
        role=user_data.role
    )


