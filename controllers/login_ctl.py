# controllers/login_controller.py
from sqlalchemy.orm import Session
from models.cliente_mod import Cliente
from models.administrador_mod import Administrador
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class LoginController:
    @staticmethod
    def login(db: Session, e_mail: str, contrasenia: str):
        user = db.query(Cliente).filter(Cliente.e_mail == e_mail).first()
        if not user:
            admin = db.query(Administrador).filter(Administrador.e_mail == e_mail).first()
            return  admin

        if not pwd_context.verify(contrasenia, user.contrasenia):
            return None  # Contraseña incorrecta

        return user  # Usuario autenticado
