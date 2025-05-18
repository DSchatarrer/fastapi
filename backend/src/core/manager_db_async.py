# backend\src\core\manager_db_async.py

from sqlalchemy.ext.asyncio import create_async_engine
from sqlmodel import SQLModel
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy.orm import sessionmaker


from .settings import settings



async_engine = create_async_engine(url=settings.SQLALCHEMY_DATABASE_URI_ASYNC,
                                    echo=False,
                                    pool_pre_ping=True,
                                    pool_recycle=1800,  # Reciclar conexiones después de 30 minutos
                                    # connect_args={"timeout": 30},  # Incrementa el tiempo de espera a 30 segundos
                                    # poolclass=AsyncAdaptedQueuePool,  # O utiliza NullPool si quieres mantenerlas al mínimo
                                    # pool_size=10,  # Número de conexiones persistentes en el pool
                                    # max_overflow=5,  # Conexiones adicionales permitidas si el pool está lleno
                                    # pool_timeout=30,  # Tiempo máximo de espera para obtener una conexión
                                )

async_session_backgroung = sessionmaker(
    bind=async_engine, class_=AsyncSession, expire_on_commit=False
)


async def init_db():
    """Create the database tables"""
    async with async_engine.begin() as conn:
        from applications.pacientes.models import Pacientes
        from core.models.sessions import Sessions
        from core.models.users import Users

        await conn.run_sync(SQLModel.metadata.create_all)

async def get_session() -> AsyncSession: # type: ignore
    """Dependency to provide the session object"""
    async_session = sessionmaker(
        bind=async_engine, class_=AsyncSession, expire_on_commit=False
    )

    async with async_session() as session:
        yield session







