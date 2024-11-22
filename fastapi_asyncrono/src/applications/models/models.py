# src\applications\models\models.py

from sqlmodel import SQLModel, Field, Column, ForeignKey
import sqlalchemy.dialects.postgresql as pg

class Model(SQLModel, table=True):
    """
    Represents a model in the database.
    """
    __tablename__ = 'models'

    model_id: int = Field(default=None, primary_key=True)
    project_id: int = Field(sa_column=Column(pg.INTEGER, ForeignKey("projects.project_id", ondelete="CASCADE"), nullable=False))
    name: str = Field(sa_column=Column(pg.VARCHAR, nullable=False))
    version: str = Field(sa_column=Column(pg.VARCHAR, nullable=False))

    def __repr__(self) -> str:
        return f"Model(model_id={self.model_id}, name='{self.name}', version='{self.version}')"
