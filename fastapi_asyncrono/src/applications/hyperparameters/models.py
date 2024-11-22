# src\applications\hyperparameters\models.py

from sqlmodel import SQLModel, Field, Column, ForeignKey
from datetime import datetime
import sqlalchemy.dialects.postgresql as pg

class Hyperparameter(SQLModel, table=True):
    """
    Represents a hyperparameter set in the database.
    """
    __tablename__ = 'hyperparameters'

    hyperparameter_id: int = Field(default=None, primary_key=True)
    prompt_id: int = Field(sa_column=Column(pg.INTEGER, ForeignKey("prompts.prompt_id", ondelete="CASCADE"), nullable=False))
    project_id: int = Field(sa_column=Column(pg.INTEGER, ForeignKey("projects.project_id", ondelete="CASCADE"), nullable=False))
    name: str = Field(sa_column=Column(pg.VARCHAR, nullable=False))
    description: str = Field(sa_column=Column(pg.TEXT, default=None))
    top_k: int = Field(sa_column=Column(pg.INTEGER, default=None))
    top_p: float = Field(sa_column=Column(pg.FLOAT, default=None))
    temperature: float = Field(sa_column=Column(pg.FLOAT, default=None))
    max_tokens: int = Field(sa_column=Column(pg.INTEGER, default=None))
    seed: int = Field(sa_column=Column(pg.INTEGER, default=None))
    created_at: datetime = Field(sa_column=Column(pg.TIMESTAMP, default=datetime.now))
    updated_at: datetime = Field(sa_column=Column(pg.TIMESTAMP, default=datetime.now, onupdate=datetime.now))

    def __repr__(self) -> str:
        return f"Hyperparameter(hyperparameter_id={self.hyperparameter_id}, name='{self.name}')"
