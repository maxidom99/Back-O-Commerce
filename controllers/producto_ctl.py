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

def update_product_db(db: Session, product_id: int, precios: float, nombres: str, id_cat: int, baja: str, descripcion: str, img_product: bytes):
    product = db.query(Producto).filter(Producto.id == product_id).first()
    if product:
        product.precios = precios
        product.nombres = nombres
        product.id_cat = id_cat
        product.baja = baja
        product.descripcion = descripcion
        product.img_product = img_product
        db.commit()
        db.refresh(product)
        return product
    return None

def busqueda_producto(id: int, db: Session):
    return db.query(Producto).filter(or_(Producto.id == id, Producto.baja == "N")).first()

def buscar_prd_nombre(db: Session, nombres: str):
    productos = db.query(Producto).filter(or_(Producto.nombres.ilike(f"%{nombres}%")), Producto.baja == "N").all()
    return productos

def get_paginated_products(db: Session, page: int = 1, page_size: int = 10):
    start_index = (page - 1) * page_size
    end_index = start_index + page_size

    products = db.query(Producto).filter(Producto.baja == 'N').offset(start_index).limit(page_size).all()
    total_products = db.query(Producto).filter(Producto.baja == 'N').count()

    return {
        "products": products,
        "total_products": total_products,
        "page": page,
        "page_size": page_size,
        "total_pages": -(-total_products // page_size)
    }