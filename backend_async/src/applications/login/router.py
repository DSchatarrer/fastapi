# backend\src\applications\login\router.py

from fastapi import (APIRouter, Depends, Response, Request, BackgroundTasks)
from sqlmodel.ext.asyncio.session import AsyncSession
from fastapi.responses import StreamingResponse
from http import HTTPStatus
from typing import Optional, List, Dict


from core.security import require_secret
from core.manager_db_async import get_session
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
    session: AsyncSession = Depends(get_session)
):
    return await LoginService(session, request.app.state.logger).login(
        response=response,
        username=credentials.usu,
        password=credentials.pwd
    )


@login_router.post("/alta-usuario", dependencies=[Depends(require_secret)])
async def create_user(
    user_data: UserCreateRequest,
    request: Request,
    session: AsyncSession = Depends(get_session)
):

    return await LoginService(session, request.app.state.logger).create_user(
        username=user_data.usu,
        password=user_data.pwd,
        role=user_data.role
    )


