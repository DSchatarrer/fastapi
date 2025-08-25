# src\applications\info_errores\controllers.py

from datetime import datetime
from sqlmodel import Session
from fastapi import HTTPException
from http import HTTPStatus
from sqlalchemy.dialects.postgresql import insert
from typing import Optional

from .models import Errores


class LogsService:
    def __init__(self, session: Session):
        self.session = session

    async def insert_error_log(self, message_id: str, location: str, buzon: Optional[str] = None, error: Optional[str] = None) -> dict:
        """
        Inserta o actualiza un registro en la tabla errores_logs.

        - Si `(message_id, location)` ya existe, actualiza `buzon`, `error` y `created_at`.
        - Si no existe, inserta un nuevo registro.
        """
        if not location:
            raise HTTPException(
                status_code=HTTPStatus.BAD_REQUEST,
                detail="El campo 'location' es obligatorio porque forma parte de la clave primaria."
            )

        try:
            insert_statement = insert(Errores).values(
                message_id=message_id,
                location=location,
                buzon=buzon,
                error=error,
                created_at=datetime.now()
            ).on_conflict_do_update(
                index_elements=["message_id", "location"],
                set_={"buzon": buzon, "error": error, "created_at": datetime.now()}
            )

            await self.session.exec(insert_statement)
            await self.session.commit()

            return {"message": "Error log registrado o actualizado exitosamente."}

        except Exception as e:
            raise HTTPException(
                status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
                detail=f"Error al insertar o actualizar error log. {e}"
            )

 