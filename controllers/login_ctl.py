# controllers/login_controller.py
from sqlalchemy.orm import Session
from models.cliente_mod import Cliente
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class LoginController:
    @staticmethod
    def login(db: Session, e_mail: str, contrasenia: str):
        user = db.query(Cliente).filter(Cliente.e_mail == e_mail).first()
        if not user:
            return None  # Usuario no encontrado

        if not pwd_context.verify(contrasenia, user.contrasenia):
            return None  # Contraseña incorrecta

        return user  # Usuario autenticado
