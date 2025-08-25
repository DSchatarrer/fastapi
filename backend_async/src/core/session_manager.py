# src\core\session_manager.py

from datetime import datetime, timezone
from sqlalchemy import delete
from sqlmodel.ext.asyncio.session import AsyncSession

from logging import Logger

from .models.sessions import Sessions
from .token_utils import get_uuid_and_exp_from_token



class SessionManager:
    def __init__(self, session: AsyncSession,  logger: Logger):
        self.session = session
        self.logger = logger

    async def create_session(self, username: str, token: str) -> Sessions:
        try:
            uuid, exp = get_uuid_and_exp_from_token(token)

            nueva_sesion = Sessions(token=uuid, usu=username, exp=exp)
            self.session.add(nueva_sesion)
            await self.session.commit()
            await self.session.refresh(nueva_sesion)

            return nueva_sesion
        except Exception as e:
            self.logger.error("Error al crear sesión: %s", e, exc_info=True)
            raise
        
    async def purge_expired_sessions(self) -> None:
        """
        Elimina todas las sesiones caducadas (exp < ahora UTC).
        """
        try:
            stmt = delete(Sessions).where(Sessions.exp < datetime.now(timezone.utc))
            result = await self.session.exec(stmt)
            await self.session.commit()
            self.logger.info("Sesiones caducadas eliminadas: %d", result.rowcount)
        except Exception as e:
            await self.session.rollback()
            self.logger.error("Error al purgar sesiones caducadas: %s", e, exc_info=True)
            raise