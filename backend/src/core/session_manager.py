# src\core\session_manager.py

from datetime import datetime, timezone
from sqlalchemy import delete
from sqlmodel import Session
from logging import Logger

from .models.sessions import Sessions
from .token_utils import get_uuid_and_exp_from_token



class SessionManager:
    def __init__(self, session: Session,  logger: Logger):
        self.session = session
        self.logger = logger

    def create_session(self, username: str, token: str) -> Sessions:
        try:
            uuid, exp = get_uuid_and_exp_from_token(token)

            nueva_sesion = Sessions(token=uuid, usu=username, exp=exp)
            self.session.add(nueva_sesion)
            self.session.commit()
            self.session.refresh(nueva_sesion)

            return nueva_sesion
        except Exception as e:
            self.logger.error("Error al crear sesión: %s", e, exc_info=True)
            raise
        
    def purge_expired_sessions(self) -> None:
        """Elimina todas las sesiones caducadas (exp < ahora UTC)."""
        try:
            stmt = delete(Sessions).where(Sessions.exp < datetime.now(timezone.utc))
            result = self.session.exec(stmt)
            self.session.commit()
            self.logger.info("Sesiones caducadas eliminadas: %d", result.rowcount)
        except Exception as e:
            self.logger.error("Error al purgar sesiones caducadas: %s", e, exc_info=True)
            raise