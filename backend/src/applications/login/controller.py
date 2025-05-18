# backend\src\applications\login\controller.py


from sqlmodel import Session, select
from fastapi import HTTPException, Response, status, Depends
from fastapi.responses import JSONResponse
from http import HTTPStatus
from logging import Logger
from typing import Optional


from core.settings import settings
from core.utils import normalize_text
from core.session_manager import SessionManager
from core.token_utils import create_token
from werkzeug.security import generate_password_hash, check_password_hash
from core.models.users import Users



class LoginService:
    def __init__(self, session: Session, logger: Logger):
        self.session = session
        self.logger = logger
        self.session_manager = SessionManager(session, logger)

    def login(self, response: Response, username: str, password: str):
        if not username or not password:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Faltan campos 'user' o 'password'"
            )

        username_normalizado = normalize_text(username).upper()

        user = self.get_user(username_normalizado)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Usuario no encontrado"
            )

        if not user.hash_pwd or not self.authenticate_user(user.hash_pwd, password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Contraseña incorrecta"
            )

        access_token = create_token()
        self.session_manager.create_session(username_normalizado, access_token)

        response.set_cookie(
            key="X-Sync.Ref",
            value=access_token,
            max_age=settings.TOKEN_SECONDS_EXP,
            httponly=True,
            samesite="lax",
            path="/"
        )

        return {"message": "Login correcto"}

    def get_user(self, username: str) -> Optional[Users]:
        try:
            statement = select(Users).where(Users.usu == username)
            result = self.session.exec(statement).first()
            return result
        except Exception as e:
            self.logger.error("Error al obtener el usuario: %s", e, exc_info=True)
            raise HTTPException(status_code=500, detail="Error interno al buscar el usuario")

    def create_user(self, username: str, password: str, role: str):
        try:
            username_normalizado = normalize_text(username)

            existing_user = self.get_user(username_normalizado)
            if existing_user:
                return JSONResponse(
                    status_code=HTTPStatus.CONFLICT,
                    content={"message": f"El usuario '{username_normalizado}' ya existe."}
                )

            hashed_pwd = generate_password_hash(password)
            user = Users(usu=username_normalizado, hash_pwd=hashed_pwd, role=role)

            self.session.add(user)
            self.session.commit()
            self.session.refresh(user)

            return JSONResponse(
                status_code=HTTPStatus.CREATED,
                content={"message": f"Usuario '{user.usu}' creado exitosamente."}
            )
        except Exception as e:
            self.logger.error("Error al crear usuario: %s", e, exc_info=True)
            raise HTTPException(status_code=500, detail="Error interno al crear el usuario")

    def authenticate_user(self, hashed_password: str, plain_password: str) -> bool:
        return check_password_hash(hashed_password, plain_password)