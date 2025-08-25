# backend\src\applications\reservas\router.py

from fastapi import (APIRouter, Depends, Response, Query, UploadFile, File, 
                     HTTPException, Form, Request, BackgroundTasks)
from sqlmodel.ext.asyncio.session import AsyncSession
from fastapi.responses import StreamingResponse
from http import HTTPStatus
from typing import Optional, List, Dict


from core.manager_db_async import get_session
from core.security import require_secret, require_roles
# from .controller import PacienteService
from .schemas import (
    PacienteNombresResponseModel,
    PacienteCreateModel,
    PacienteUpdateModel,
    PacienteResponseModel
)


reservas_router = APIRouter(
    prefix="/reservas",
    tags=["reservas"],
    dependencies=[Depends(require_roles("papi"))], 
    # dependencies=[Depends(require_secret),
    #               Depends(lambda request: require_auth(request, roles=["admin", "medico"]))],
)


@reservas_router.get("/nombres")
async def get_paciente_names(request: Request, session: AsyncSession = Depends(get_session)):
    """
    Endpoint para obtener la lista de nombres de todos los pacientes.

    Returns:
        List[str]: Lista con los nombres de usuario de los pacientes.
    """
    # return PacienteService(session, request.app.state.logger).get_all_paciente_names()
    return {"acceso": "ok"}


# @paciente_router.post("/add", response_model=PacienteResponseModel)
# async def create_paciente(
#     data: PacienteCreateModel,
#     request: Request,
#     session: AsyncSession = Depends(get_session)
# ):
#     """
#     Crea un nuevo paciente.
#     """
#     return PacienteService(session, request.app.state.logger).create_paciente(data)


# @paciente_router.put("/update/{paciente_id}", response_model=PacienteResponseModel)
# async def update_paciente(
#     paciente_id: int,
#     data: PacienteUpdateModel,
#     request: Request,
#     session: AsyncSession = Depends(get_session)
# ):
#     """
#     Actualiza los datos de un paciente existente.
#     """
#     return PacienteService(session, request.app.state.logger).update_paciente(paciente_id, data)


# @paciente_router.delete("/remove/{paciente_id}")
# async def delete_paciente(
#     paciente_id: int,
#     request: Request,
#     session: AsyncSession = Depends(get_session)
# ):
#     """
#     Elimina un paciente por su ID.
#     """
#     return PacienteService(session, request.app.state.logger).delete_paciente(paciente_id)