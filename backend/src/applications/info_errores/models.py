# src\applications\info_errores\models.py

from sqlmodel import SQLModel, Field, Column
from datetime import datetime
from sqlalchemy import func
import sqlalchemy.dialects.postgresql as pg

class Errores(SQLModel, table=True):
    """
    Representa un registro de error en la base de datos.
    """
    __tablename__ = 'errores_logs'

    message_id: str = Field(sa_column=Column(pg.VARCHAR(255), primary_key=True, nullable=False))
    location: str = Field(sa_column=Column(pg.VARCHAR(255), primary_key=True, nullable=False))
    buzon: str = Field(sa_column=Column(pg.VARCHAR(255), nullable=True))
    error: str = Field(sa_column=Column(pg.TEXT, nullable=True))
    created_at: datetime = Field(sa_column=Column(pg.TIMESTAMP(timezone=True), server_default=func.now()))

    def __repr__(self) -> str:
        return f"Errores(message_id='{self.message_id}', location='{self.location}', buzon='{self.buzon}', error='{self.error}', created_at='{self.created_at}')"

