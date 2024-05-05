import bcrypt
from models.user_mod import Usuario
from passlib.context import CryptContext
import re
from sqlalchemy.orm import Session
from sqlalchemy import or_, and_

def create_user_db(db: Session, documento: str, nombre: str, apellido: str, e_mail: str, contrasenia: str, baja: str, img_perfil: bytes, rol: str):
    existing_user_email = db.query(Usuario).filter(Usuario.e_mail == e_mail).first()
    if existing_user_email:
        return None, "El correo electrónico ya está registrado"

    existing_user_doc = db.query(Usuario).filter(Usuario.documento == documento).first()
    if existing_user_doc:
        return None, "El documento ya está registrado"

    if not re.match(r'^[a-zA-Z]{2,}@[a-zA-Z]{2,}\.[a-zA-Z]{2,}$', e_mail):
        return None, "El correo electrónico no cumple con el formato requerido"

    if not re.match(r'^(?=.*\d)(?=.*[a-z])(?=.*[A-Z])(?=.*[!@#$%^&*()-_+=<>,.?/:;{}[\]|~])(?!.*\s).{8,}$', contrasenia):
        return None, "La contraseña debe tener al menos 8 caracteres y contener al menos un número, una letra mayúscula, una letra minúscula y un símbolo"

    hashed_password = bcrypt.hashpw(contrasenia.encode('utf-8'), bcrypt.gensalt())

    new_user_data = {
        "documento": documento,
        "nombre": nombre,
        "apellido": apellido,
        "e_mail": e_mail,
        "contrasenia": hashed_password.decode('utf-8'),
        "baja": baja,
        "img_perfil": img_perfil,
        "rol": rol
    }

    new_user = Usuario(**new_user_data)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user, "Usuario creado exitosamente"


def update_user_db(db: Session, id: int, documento: str, nombre: str, apellido: str, e_mail: str, contrasenia: str, baja: str, img_perfil: bytes, rol: str):
    user = db.query(Usuario).filter(or_(Usuario.id == id), Usuario.baja == "N").first()
    if user:
        user.documento = documento
        user.nombre = nombre
        user.apellido = apellido
        if not re.match(r'^[a-zA-Z]{2,}@[a-zA-Z]{2,}\.[a-zA-Z]{2,}$', e_mail):
            return None, "El correo electrónico no cumple con el formato requerido"
        user.e_mail = e_mail
        if contrasenia:
            if not re.match(r'^(?=.*\d)(?=.*[a-z])(?=.*[A-Z])(?=.*[!@#$%^&*()-_+=<>,.?/:;{}[\]|~])(?!.*\s).{8,}$', contrasenia):
                return None, "La contraseña debe tener al menos 8 caracteres y contener al menos un número, una letra mayúscula, una letra minúscula y un símbolo"
            hashed_password = bcrypt.hashpw(contrasenia.encode('utf-8'), bcrypt.gensalt())
            user.contrasenia = hashed_password.decode('utf-8')
        user.baja = baja
        user.img_perfil = img_perfil
        user.rol = rol
        db.commit()
        db.refresh(user)
        return user, "Usuario actualizado exitosamente"
    return None, "Usuario no encontrado"


def buscar_usr_nombre(db: Session, nombre: str):
    Usuarios = db.query(Usuario).filter(or_(Usuario.nombre.ilike(f"%{nombre}%")), Usuario.baja == "N").all()
    return Usuarios

def busqueda_user(id: int, db: Session):
    return db.query(Usuario).filter(or_(Usuario.id == id), Usuario.baja == "N").first()

class LoginController:
    @staticmethod
    def login(db: Session, e_mail: str, contrasenia: str):
        res = None
        user = db.query(Usuario).filter(and_(Usuario.e_mail == e_mail), Usuario.baja == "N").first()
        if user:
            pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
            if pwd_context.verify(contrasenia, user.contrasenia):
                res = user

        return res