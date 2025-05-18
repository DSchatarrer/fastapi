# backend\src\core\manager_db_sync.py

from functools import wraps
from sqlmodel import Session, SQLModel, create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import QueuePool, NullPool, AsyncAdaptedQueuePool
from typing import Generator


from .settings import settings


engine = create_engine(url=settings.SQLALCHEMY_DATABASE_URI,
                       echo=False,
                       pool_pre_ping=True,
                       pool_recycle=1800,
                    #    connect_args={"timeout": 30},  # Incrementa el tiempo de espera a 30 segundos
                    #    poolclass=QueuePool,  # O utiliza NullPool si quieres mantenerlas al mínimo
                    #    max_overflow=5,  # Conexiones adicionales permitidas si el pool está lleno
                    #    pool_timeout=30,  # Tiempo máximo de espera para obtener una conexión
                       
                       )

SessionLocal = sessionmaker(bind=engine, class_=Session, expire_on_commit=False)

def init_db():
    from applications.pacientes.models import Pacientes
    from core.models.sessions import Sessions
    from core.models.users import Users
        
    with engine.begin() as conn:
        SQLModel.metadata.create_all(conn)

def get_session() -> Generator[Session, None, None]:
    with SessionLocal() as session:
        yield session








