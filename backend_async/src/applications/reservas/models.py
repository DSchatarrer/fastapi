# backend\src\applications\reservas\models.py

from typing import Optional
from datetime import datetime
from sqlmodel import SQLModel, Field, Relationship, Column, ForeignKey, PrimaryKeyConstraint
from sqlalchemy import func, CheckConstraint
import sqlalchemy.dialects.postgresql as pg


class Pacientes(SQLModel, table=True):
    """
    Represents a pacientes in the database.
    """
    __tablename__ = 'n_pacientes'   
    
    id: int = Field(default=None, primary_key=True)
    username: str = Field(sa_column=Column(pg.VARCHAR(355), nullable=False, unique=True, index=True))
    fecha_creacion: datetime = Field(sa_column=Column(pg.TIMESTAMP(timezone=True), server_default=func.now()))
    created_modificacion: datetime = Field(sa_column=Column(pg.TIMESTAMP(timezone=True),server_default=func.now(),server_onupdate=func.now(),nullable=False))

    def __repr__(self) -> str:
        return f"Pacientes(username='{self.username}', fecha_creacion='{self.fecha_creacion}')"
    
