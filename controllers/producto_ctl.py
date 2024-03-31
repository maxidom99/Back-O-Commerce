from sqlalchemy.orm import Session
from fastapi import UploadFile
from models.producto_mod import Producto
from sqlalchemy import or_

def create_product_db(db: Session, precios: float, nombres: str, id_cat: int, baja: str, descripcion: str, img_product: bytes):
    new_product_data = {"precios": precios, "nombres": nombres, "id_cat": id_cat, "baja": baja, "descripcion": descripcion, "img_product": img_product}
    new_product = Producto(**new_product_data)
    db.add(new_product)
    db.commit()
    db.refresh(new_product)
    return new_product

def update_product_db(db: Session, id:int, **data):
    db_product = db.query(Producto).filter(or_(Producto.id == id), Producto.baja == "N").first()
    if db_product:
        for k, v in data.items():
            if v is not None:
                setattr(db_product, k, v)
        
        db.commit()
        db.refresh(db_product)
        
        return db_product
    return None

def busqueda_producto(id: int, db: Session):
    return db.query(Producto).filter(or_(Producto.id == id, Producto.baja == "N")).first()

def buscar_prd_nombre(db: Session, nombres: str):
    productos = db.query(Producto).filter(or_(Producto.nombres.ilike(f"%{nombres}%")), Producto.baja == "N").all()
    return productos