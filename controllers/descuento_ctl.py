from sqlalchemy.orm import Session
from sqlalchemy import or_
from models.descuento_mod import Descuento

def create_dsc_db(db: Session, nombre: str, baja: str, descripcion: str):
    new_discount_data = {"nombre": nombre, "baja": baja, "descripcion": descripcion}
    new_discount = Descuento(**new_discount_data)
    db.add(new_discount)
    db.commit()
    db.refresh(new_discount)
    return new_discount

def update_discount_db(db: Session, id:int, **data):
    db_discount = db.query(Descuento).filter(or_(Descuento.id == id), Descuento.baja == "N").first()
    if db_discount:
        for k, v in data.items():
            if v is not None:
                setattr(db_discount, k, v)
        
        db.commit()
        db.refresh(db_discount)
        
        return db_discount
    return None

def busqueda_descuento(id: int, db: Session):
    return db.query(Descuento).filter(or_(Descuento.id == id), Descuento.baja == "N").first()

def buscar_dsc_nombre(db: Session, nombre: str):
    descuentos = db.query(Descuento).filter(or_(Descuento.nombre.ilike(f"%{nombre}%")), Descuento.baja == "N").all()
    return descuentos