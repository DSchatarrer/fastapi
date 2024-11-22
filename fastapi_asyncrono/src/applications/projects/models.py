# src\applications\projects\models.py

from sqlmodel import SQLModel, Field, Column
import sqlalchemy.dialects.postgresql as pg

class Project(SQLModel, table=True):
    """
    Represents a project in the database.
    """
    __tablename__ = 'projects'
    
    project_id: int = Field(default=None, primary_key=True)
    name: str = Field(sa_column=Column(pg.VARCHAR, nullable=False))

    def __repr__(self) -> str:
        return f"Project(project_id={self.project_id}, name='{self.name}')"
