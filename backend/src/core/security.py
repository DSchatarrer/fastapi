# backend\src\core\security.py


from datetime import datetime, timezone
from sqlmodel import Session, select
from fastapi import  HTTPException, Query, Depends, Request
from http import HTTPStatus
from typing import Optional, Dict, Any, List


from .settings import settings
from .manager_db_sync import get_session
from .session_manager import SessionManager
from .token_utils import verify_token
from .models.sessions import Sessions
from .models.users import Users


async def require_secret(secret: str = Query(...)):
    if secret != settings.API_KEY:
        raise HTTPException(
            status_code=HTTPStatus.UNAUTHORIZED,
            detail="No autorizado: clave secreta incorrecta"
        )

async def require_auth(
    request: Request,
    roles: Optional[List[str]] = None, 
    session: Session = Depends(get_session),
) -> Dict[str, Any]:
    """
    Autenticación basada en la cookie `X-Sync.Ref`.

    - Valida el JWT y la sesión en BD.
    - Opcionalmente comprueba que el usuario tenga alguno de los `roles`.
    """
    SessionManager(session, request.app.state.logger).purge_expired_sessions()

    token_cookie = request.cookies.get("X-Sync.Ref")
    if not token_cookie:
        raise HTTPException(
            status_code=HTTPStatus.UNAUTHORIZED,
            detail="No se encontró la cookie de autenticación",
        )

    try:
        payload = verify_token(token_cookie)
    except ValueError as e:
        raise HTTPException(
            status_code=HTTPStatus.UNAUTHORIZED,
            detail=str(e),
        )

    uuid_ = payload.get("sub")
    if not uuid_:
        raise HTTPException(
            status_code=HTTPStatus.UNAUTHORIZED,
            detail="Token sin identificador de sesión (sub)",
        )

    sesion = session.exec(
        select(Sessions).where(Sessions.token == uuid_)
    ).first()

    if not sesion:
        raise HTTPException(
            status_code=HTTPStatus.UNAUTHORIZED,
            detail="Sesión no encontrada o inválida",
        )

    if sesion.exp < datetime.now(timezone.utc):
        raise HTTPException(
            status_code=HTTPStatus.UNAUTHORIZED,
            detail="Sesión expirada",
        )

    if roles is not None:
        user = session.exec(
            select(Users).where(Users.usu == sesion.usu)
        ).first()

        if not user or user.role not in roles:
            raise HTTPException(
                status_code=HTTPStatus.FORBIDDEN,
                detail="Permisos insuficientes para este recurso",
            )

    return {
        "username": sesion.usu,
        "uuid": uuid_,
        "token_payload": payload,
    }


# 2) Factory para fijar roles en routers o endpoints --------------------------
def require_roles(*roles: str):
    """
    Devuelve una dependencia `require_auth` con los `roles` indicados.
    Ejemplo:   dependencies=[Depends(require_roles("admin", "medico"))]
    """
    async def _dep(
        request: Request,
        session: Session = Depends(get_session),
    ):
        return await require_auth(request, roles=list(roles), session=session)

    return _dep          



