# src\applications\prompts\models.py

from sqlmodel import SQLModel, Field, Column, ForeignKey
from datetime import datetime
import sqlalchemy.dialects.postgresql as pg

class Prompt(SQLModel, table=True):
    """
    Represents a prompt in the database.
    """
    __tablename__ = 'prompts'

    prompt_id: int = Field(default=None, primary_key=True)
    model_id: int = Field(sa_column=Column(pg.INTEGER, ForeignKey("models.model_id", ondelete="CASCADE"), nullable=False))
    project_id: int = Field(sa_column=Column(pg.INTEGER, ForeignKey("projects.project_id", ondelete="CASCADE"), nullable=False))
    name: str = Field(sa_column=Column(pg.VARCHAR, nullable=False))
    description: str = Field(sa_column=Column(pg.TEXT, default=None))
    prompt_text: str = Field(sa_column=Column(pg.TEXT, nullable=False))
    created_at: datetime = Field(sa_column=Column(pg.TIMESTAMP, default=datetime.now))
    updated_at: datetime = Field(sa_column=Column(pg.TIMESTAMP, default=datetime.now, onupdate=datetime.now))

    def __repr__(self) -> str:
        return f"Prompt(prompt_id={self.prompt_id}, name='{self.name}')"
