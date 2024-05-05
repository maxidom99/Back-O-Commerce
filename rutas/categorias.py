from fastapi import APIRouter, HTTPException, Depends
from models.categoria_mod import *
from controllers.categoria_ctl import *
from models.database import get_db
from sqlalchemy.orm import Session

categorias = APIRouter()

@categorias.get("/categorias")
async def busqueda_categorias(db: Session = Depends(get_db)):
    categoria = db.query(Categoria).filter(Categoria.baja == 'N').all()
    return categoria

@categorias.get("/categorias/{categoria_id}")
async def busqueda_cat_id(categoria_id: int, db: Session = Depends(get_db)):
    cat_id = busqueda_cat(categoria_id, db)
    if cat_id is None:
        raise HTTPException(status_code=404, detail="Categoría no encontrada.")
    return cat_id

@categorias.get("/category/{nombre}")
async def busqueda_cat_nombre(nombre: str, db: Session = Depends(get_db)):
    name_cat = buscar_name_cat(db, nombre)
    if name_cat is not None:
        return name_cat
    else:
        raise HTTPException(status_code=404, detail="Categoría no encontrada.")

@categorias.post("/creando_categoria", response_model=CategoryCreate)
async def create_category(category: CategoryCreate, db: Session = Depends(get_db)):
    return create_category_db(db, **category.dict())

@categorias.put("/mod_category/{categoria_id}", response_model=ResultadoActCat)
async def update_category(categoria_id: int, category: CategoryUpdate, db: Session = Depends(get_db)):
    cat_existe = busqueda_cat(categoria_id, db)
    if cat_existe is None:
        raise HTTPException(status_code=404, detail="Categoría no encontrada.")
    
    modificacion = update_category_db(db, categoria_id, **category.dict())
    if modificacion:
        return ResultadoActCat(message="Categoría actualizada correctamente.")
    else:
        raise HTTPException(status_code=404, detail="No se pudo actualizar la categoría.")