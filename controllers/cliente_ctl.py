from sqlalchemy.orm import Session
from sqlalchemy import or_
from models.cliente_mod import Cliente
import bcrypt

def create_client_db(db: Session, documento: str, nombre: str, apellido: str, e_mail: str, contrasenia: str, baja: str, img_perfil: str):
    hashed_password = bcrypt.hashpw(contrasenia.encode('utf-8'), bcrypt.gensalt())
    new_client_data = {"documento": documento, "nombre": nombre, "apellido": apellido, "e_mail": e_mail, "contrasenia": hashed_password.decode('utf-8'), "baja": baja, "img_perfil": img_perfil}
    new_client = Cliente(**new_client_data)
    db.add(new_client)
    db.commit()
    db.refresh(new_client)
    return new_client

def update_client_db(db: Session, id: int, **data):
    db_client = db.query(Cliente).filter(or_(Cliente.id == id), Cliente.baja == "N").first()
    if db_client:
        for k, v in data.items():
            if v is not None:
                setattr(db_client, k, v)
                
        db.commit()
        db.refresh(db_client)
        
        return db_client
    return None

def buscar_cli_nombre(db: Session, nombre: str):
    clientes = db.query(Cliente).filter(or_(Cliente.nombre.ilike(f"%{nombre}%")), Cliente.baja == "N").all()
    return clientes

def busqueda_cliente(id: int, db: Session):
    return db.query(Cliente).filter(or_(Cliente.id == id), Cliente.baja == "N").first()