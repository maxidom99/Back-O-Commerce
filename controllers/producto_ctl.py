from fastapi import UploadFile
from models.producto_mod import Producto, ProductoCreate, Ventas, VentaCreate
from sqlalchemy import or_
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from typing import Optional

def create_product_db(db: Session, producto: ProductoCreate):
    new_product_data = {
        "precios": producto.precios,
        "nombres": producto.nombres,
        "id_cat": producto.id_cat,
        "baja": producto.baja,
        "descripcion": producto.descripcion,
        "img_product": producto.img_product
    }
    new_product = Producto(**new_product_data)
    
    try:
        db.add(new_product)
        db.commit()
        db.refresh(new_product)
        return {"message": "Producto creado exitosamente", "product": new_product}, 201
    except IntegrityError as e:
        db.rollback()
        if "Duplicate entry" in str(e.orig):
            return {"error": "Ya existe un producto con el mismo nombre"}, 400
        else:
            raise e
        
def create_sell_db(db: Session, venta: VentaCreate):
    new_sell_data = {
        "fecha_venta": venta.fecha_venta,
        "id_producto": venta.id_producto,
        "id_usuario": venta.id_usuario,
    }
    new_sell = Ventas(**new_sell_data)
    
    try:
        db.add(new_sell)
        db.commit()
        db.refresh(new_sell)
        return {"message": "Venta exitosa", "venta": new_sell}, 201
    except IntegrityError as e:
        db.rollback()
        if "Duplicate entry" in str(e.orig):
            return {"error": "Venta duplicada"}, 400
        else:
            raise e

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

def purchased_product(id: int, db: Session, precios: float, nombres:str, img_product: bytes):
    product = db.query(Producto).filter(Producto.id == id).first()
    if product:
        product.precios = precios
        product.nombres = nombres
        product.img_product = img_product
    return db.query(Producto).filter(or_(Producto.id == id, Producto.baja == "N")).all()

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