from sqlalchemy.orm import Session
from sqlalchemy import or_
from models.categoria_mod import Categoria

def create_category_db(db: Session, nombre: str, baja: str, img_category: bytes):
    new_category_data = {"nombre": nombre, "baja": baja, "img_category": img_category}
    new_category = Categoria(**new_category_data)
    db.add(new_category)
    db.commit()
    db.refresh(new_category)
    return new_category

def update_category_db(db: Session, id_cat: int, nombre: str, baja: str, img_category: bytes):
    category = db.query(Categoria).filter(Categoria.id_cat == id_cat).first()
    if category:
        category.nombre = nombre
        category.baja = baja
        category.img_category = img_category
        db.commit()
        db.refresh(category)
        return category
    return None

def busqueda_cat(id_cat: int, db: Session):
    return db.query(Categoria).filter(or_(Categoria.id_cat == id_cat),Categoria.baja == "N").first()

def buscar_name_cat(db: Session, nombre: str):
    categorias = db.query(Categoria).filter(or_(Categoria.nombre.ilike(f"%{nombre}%")), Categoria.baja == "N").all()
    return categorias