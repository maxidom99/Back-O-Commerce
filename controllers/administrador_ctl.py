from sqlalchemy.orm import Session
from sqlalchemy import or_
from models.administrador_mod import Administrador

def create_admin_db(db: Session, nombre: str, apellido: str, e_mail: str, contrasenia: str, baja: str):
    new_admin_data = {"nombre": nombre, "apellido": apellido, "e_mail": e_mail, "contrasenia": contrasenia, "baja": baja}
    new_admin = Administrador(**new_admin_data)
    db.add(new_admin)
    db.commit()
    db.refresh(new_admin)
    return new_admin

def update_admin_db(db: Session, id:int, **data):
    db_admin = db.query(Administrador).filter(or_(Administrador.id == id),Administrador.baja == "N").first()
    if db_admin:
        for k, v in data.items():
            if v is not None:
                setattr(db_admin, k, v)
        
        db.commit()
        db.refresh(db_admin)
        
        return db_admin
    return None

def busqueda_adm(id: int, db: Session):
    return db.query(Administrador).filter(or_(Administrador.id == id),Administrador.baja == "N").first()

def buscar_name_adm(db: Session, nombre: str):
    administradores = db.query(Administrador).filter(or_(Administrador.nombre.ilike(f"%{nombre}%")), Administrador.baja == "N").all()
    return administradores