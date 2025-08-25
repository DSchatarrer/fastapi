# backend\src\applications\reservas\controller.py

from datetime import datetime, timezone
from sqlmodel import Session, select
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException, Request, BackgroundTasks
from logging import Logger
from http import HTTPStatus
from sqlalchemy.exc import SQLAlchemyError, OperationalError
from typing import Dict, List, Any

from core.utils import normalize_text
from .models import Pacientes
from .schemas import (
    PacienteCreateModel,
    PacienteUpdateModel,
    PacienteResponseModel
)


class PacienteService:
    def __init__(self, session: Session, logger: Logger):
        self.session = session
        self.logger = logger

    def get_all_paciente_names(self) -> Dict[str, List[Dict[str, Any]]]:
        try:
            statement = select(Pacientes.id, Pacientes.username)
            results = self.session.exec(statement)
            nombres = results.all()
            return {"nombres": [{"id": id, "username": username} for id, username in nombres]}
        except OperationalError as oe:
            self.logger.error("Error de conexión a la base de datos: %s", oe, exc_info=True)
            raise HTTPException(
                status_code=HTTPStatus.SERVICE_UNAVAILABLE,
                detail="No se pudo conectar con la base de datos. Inténtelo más tarde."
            )
        except SQLAlchemyError as db_err:
            self.logger.error("Error SQL: %s", db_err, exc_info=True)
            raise HTTPException(
                status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
                detail="Error al consultar los nombres de los pacientes."
            )
        except Exception as e:
            self.logger.critical("Error inesperado: %s", e, exc_info=True)
            raise HTTPException(
                status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
                detail="Error inesperado al obtener los nombres de los pacientes."
            )

    def create_paciente(self,
        paciente_data: PacienteCreateModel,
    ) -> PacienteResponseModel:
        try:
            username_normalizado = normalize_text(paciente_data.username)

            nuevo_paciente = Pacientes(username=username_normalizado)

            self.session.add(nuevo_paciente)
            self.session.commit()
            self.session.refresh(nuevo_paciente)

            return PacienteResponseModel.model_validate(nuevo_paciente)

        except IntegrityError:
            self.session.rollback()
            self.logger.warning(f"Username duplicado: {paciente_data.username}")
            raise HTTPException(
                status_code=HTTPStatus.CONFLICT,
                detail="Ya existe un paciente con ese nombre de usuario."
            )
        except (SQLAlchemyError, OperationalError) as e:
            self.session.rollback()
            self.logger.error(f"Error al crear paciente: {e}")
            raise HTTPException(
                status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
                detail="Error al crear el paciente."
            )

    def update_paciente(self, paciente_id: int, data: PacienteUpdateModel) -> PacienteResponseModel:
        try:
            paciente = self.session.get(Pacientes, paciente_id)
            if not paciente:
                raise HTTPException(status_code=404, detail="Paciente no encontrado.")

            update_data = data.model_dump(exclude_unset=True)
            
            if "username" in update_data:
                update_data["username"] = normalize_text(update_data["username"])

            for field, value in update_data.items():
                setattr(paciente, field, value)

            paciente.created_modificacion = datetime.now(timezone.utc)
            self.session.add(paciente)
            self.session.commit()
            self.session.refresh(paciente)

            return PacienteResponseModel.model_validate(paciente)

        except OperationalError as oe:
            self.logger.error("Error de conexión: %s", oe, exc_info=True)
            raise HTTPException(
                status_code=HTTPStatus.SERVICE_UNAVAILABLE,
                detail="No se pudo conectar con la base de datos."
            )
        except SQLAlchemyError as db_err:
            self.logger.error("Error SQL: %s", db_err, exc_info=True)
            raise HTTPException(
                status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
                detail="Error al actualizar el paciente."
            )
        except Exception as e:
            self.logger.critical("Error inesperado: %s", e, exc_info=True)
            raise HTTPException(
                status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
                detail="Error inesperado al actualizar el paciente."
            )

    def delete_paciente(self, paciente_id: int) -> Dict[str, str]:
        try:
            paciente = self.session.get(Pacientes, paciente_id)
            if not paciente:
                raise HTTPException(status_code=404, detail="Paciente no encontrado.")

            self.session.delete(paciente)
            self.session.commit()
            return {"message": "Paciente eliminado correctamente."}
        except OperationalError as oe:
            self.logger.error("Error de conexión: %s", oe, exc_info=True)
            raise HTTPException(
                status_code=HTTPStatus.SERVICE_UNAVAILABLE,
                detail="No se pudo conectar con la base de datos."
            )
        except SQLAlchemyError as db_err:
            self.logger.error("Error SQL: %s", db_err, exc_info=True)
            raise HTTPException(
                status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
                detail="Error al eliminar el paciente."
            )
        except Exception as e:
            self.logger.critical("Error inesperado: %s", e, exc_info=True)
            raise HTTPException(
                status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
                detail="Error inesperado al eliminar el paciente."
            )