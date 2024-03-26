from sqlalchemy.orm import Session
from sqlalchemy import or_
from models.categoria_mod import Categoria

def create_category_db(db: Session, nombre: str, baja: str):
    new_category_data = {"nombre": nombre, "baja": baja}
    new_category = Categoria(**new_category_data)
    db.add(new_category)
    db.commit()
    db.refresh(new_category)
    return new_category

def update_category_db(db: Session, id_cat:int, **data):
    db_category = db.query(Categoria).filter(or_(Categoria.id_cat == id_cat),Categoria.baja == "N").first()
    if db_category:
        for k, v in data.items():
            if v is not None:
                setattr(db_category, k, v)
        
        db.commit()
        db.refresh(db_category)
        
        return db_category
    return None

def busqueda_cat(id_cat: int, db: Session):
    return db.query(Categoria).filter(or_(Categoria.id_cat == id_cat),Categoria.baja == "N").first()

def buscar_name_cat(db: Session, nombre: str):
    categorias = db.query(Categoria).filter(or_(Categoria.nombre.ilike(f"%{nombre}%")), Categoria.baja == "N").all()
    return categorias