from fastapi import APIRouter, HTTPException, Depends
from models.producto_mod import *
from controllers.producto_ctl import *
from database import get_db
from sqlalchemy.orm import Session

productos = APIRouter()

@productos.get("/productos")
async def busqueda_productos(db: Session = Depends(get_db)):
    productos = db.query(Producto).filter(Producto.baja == 'N').all()
    return productos

@productos.get("/productos/{produ_id}")
async def busqueda_prd_id(produ_id: int, db: Session = Depends(get_db)):
    prd_id = busqueda_producto(produ_id, db)
    if prd_id is None:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    return prd_id

@productos.get("/product/{nombres}")
async def buscar_product_nombre(nombres: str, db: Session = Depends(get_db)):
    producto_encontrado = buscar_prd_nombre(db, nombres)
    if producto_encontrado is not None:
        return producto_encontrado
    else:
        raise HTTPException(status_code=404, detail="Producto no encontrado")

@productos.post("/alta_productos", response_model=ProductoCreate)
async def create_product(producto: ProductoCreate, db: Session = Depends(get_db)):
    return create_product_db(db, **producto.dict())

@productos.put("/mod_produ/{id}", response_model=ResultadoAct)
async def update_product(id: int, producto: ProductoUpdate, db: Session = Depends(get_db)):
    prd_existe = busqueda_producto(id, db)
    if prd_existe is None:
        raise HTTPException(status_code=404, detail="Producto no encontrado.")
    
    modificacion = update_product_db(db, id, **producto.dict())
    if modificacion:
        return ResultadoAct(message="Producto actualizado correctamente.")
    else:
        raise HTTPException(status_code=404, detail="No se pudo actualizar el producto")