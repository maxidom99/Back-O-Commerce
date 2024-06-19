import bcrypt
from models.user_mod import Usuario
from models.user_mod import UserCreate
from passlib.context import CryptContext
import re
from sqlalchemy.orm import Session
from sqlalchemy import or_, and_
from typing import Optional

def create_user_db(db: Session, user: UserCreate):
    existing_user_email = db.query(Usuario).filter(Usuario.e_mail == user.e_mail).first()
    if existing_user_email:
        return {"error": "El correo electrónico ya está registrado"}, 400

    existing_user_doc = db.query(Usuario).filter(Usuario.documento == user.documento).first()
    if existing_user_doc:
        return {"error": "El documento ya está registrado"}, 400

    if not re.match(r'^[a-zA-Z]{2,}@[a-zA-Z]{2,}\.[a-zA-Z]{2,}$', user.e_mail):
        return {"error": "El correo electrónico no cumple con el formato requerido"}, 400

    if not re.match(r'^(?=.*\d)(?=.*[a-z])(?=.*[A-Z])(?=.*[!@#$%^&*()-_+=<>,.?/:;{}[\]|~])(?!.*\s).{8,}$', user.contrasenia):
        return {"error": "La contraseña debe tener al menos 8 caracteres y contener al menos un número, una letra mayúscula, una letra minúscula y un símbolo"}, 400

    hashed_password = bcrypt.hashpw(user.contrasenia.encode('utf-8'), bcrypt.gensalt())

    new_user_data = {
        "documento": user.documento,
        "nombre": user.nombre,
        "apellido": user.apellido,
        "e_mail": user.e_mail,
        "contrasenia": hashed_password.decode('utf-8'),
        "baja": user.baja,
        "img_perfil": user.img_perfil,
        "rol": user.rol
    }

    new_user = Usuario(**new_user_data)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return {"message": "Usuario creado exitosamente", "user": new_user}, 201


def update_user_db(db: Session, id: int, documento: Optional[str], nombre: Optional[str], apellido: Optional[str], e_mail: Optional[str], contrasenia: Optional[str], baja: Optional[str], img_perfil: Optional[bytes], rol: Optional[str]):
    user = db.query(Usuario).filter(or_(Usuario.id == id), Usuario.baja == "N").first()
    if user:
        if documento is not None:
            user.documento = documento
        if nombre is not None:
            user.nombre = nombre
        if apellido is not None:
            user.apellido = apellido
        if e_mail is not None:
            if not re.match(r'^[a-zA-Z]{2,}@[a-zA-Z]{2,}\.[a-zA-Z]{2,}$', e_mail):
                return None, "El correo electrónico no cumple con el formato requerido"
            user.e_mail = e_mail
        if contrasenia is not None:
            if not re.match(r'^(?=.*\d)(?=.*[a-z])(?=.*[A-Z])(?=.*[!@#$%^&*()-_+=<>,.?/:;{}[\]|~])(?!.*\s).{8,}$', contrasenia):
                return None, "La contraseña debe tener al menos 8 caracteres y contener al menos un número, una letra mayúscula, una letra minúscula y un símbolo"
            hashed_password = bcrypt.hashpw(contrasenia.encode('utf-8'), bcrypt.gensalt())
            user.contrasenia = hashed_password.decode('utf-8')
        if baja is not None:
            user.baja = baja
        if img_perfil is not None:
            user.img_perfil = img_perfil
        if rol is not None:
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