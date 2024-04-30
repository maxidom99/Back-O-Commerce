from sqlalchemy.orm import Session
from sqlalchemy import or_
from models.user_mod import Usuario
import bcrypt

def create_user_db(db: Session, documento: str, nombre: str, apellido: str, e_mail: str, contrasenia: str, baja: str, img_perfil: str, rol: str):
    hashed_password = bcrypt.hashpw(contrasenia.encode('utf-8'), bcrypt.gensalt())
    new_user_data = {"documento": documento, "nombre": nombre, "apellido": apellido, "e_mail": e_mail, "contrasenia": hashed_password.decode('utf-8'), "baja": baja, "img_perfil": img_perfil, "rol": rol}
    new_user = Usuario(**new_user_data)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

def update_user_db(db: Session, id: int, **data):
    db_user = db.query(Usuario).filter(or_(Usuario.id == id), Usuario.baja == "N").first()
    if db_user:
        for k, v in data.items():
            if v is not None:
                setattr(db_user, k, v)
                
        db.commit()
        db.refresh(db_user)
        
        return db_user
    return None

def buscar_usr_nombre(db: Session, nombre: str):
    Usuarios = db.query(Usuario).filter(or_(Usuario.nombre.ilike(f"%{nombre}%")), Usuario.baja == "N").all()
    return Usuarios

def busqueda_user(id: int, db: Session):
    return db.query(Usuario).filter(or_(Usuario.id == id), Usuario.baja == "N").first()