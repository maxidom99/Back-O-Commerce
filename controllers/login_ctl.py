# controllers/login_controller.py
from sqlalchemy.orm import Session
from models.user_mod import Usuario
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class LoginController:
    @staticmethod
    def login(db: Session, e_mail: str, contrasenia: str):
        user = db.query(Usuario).filter(Usuario.e_mail == e_mail).first()
        if db.query(Usuario).filter(Usuario.rol == "C"):
            return user
        elif db.query(Usuario).filter(Usuario.rol == "A"):
            return user
      

        if not pwd_context.verify(contrasenia, user.contrasenia):
            return None  # Contraseña incorrecta

        return user  # Usuario autenticado
