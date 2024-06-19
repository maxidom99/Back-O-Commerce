from sqlalchemy.orm import Session
from sqlalchemy import or_
from models.categoria_mod import Categoria, CategoryCreate

def create_category_db(db: Session, category: CategoryCreate):
    # Validaciones si fueran necesarias, p. ej., nombres únicos, etc.
    existing_category = db.query(Categoria).filter(Categoria.nombre == category.nombre).first()
    if existing_category:
        return {"error": "El nombre de la categoría ya está registrado"}, 400

    new_category_data = {
        "nombre": category.nombre,
        "baja": category.baja,
        "img_category": category.img_category
    }

    new_category = Categoria(**new_category_data)
    db.add(new_category)
    db.commit()
    db.refresh(new_category)

    return {"message": "Categoría creada exitosamente", "category": new_category}, 201

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