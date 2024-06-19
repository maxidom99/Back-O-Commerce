from fastapi import APIRouter, HTTPException, Depends, Query, status
from models.producto_mod import *
from controllers.producto_ctl import *
from models.database import get_db
from sqlalchemy.orm import Session

productos = APIRouter()

@productos.get("/productos")
async def busqueda_productos(db: Session = Depends(get_db)):
    productos = db.query(Producto).filter(Producto.baja == 'N').all()
    return productos

@productos.get("/productos_pages")
async def busqueda_productos(page: int = Query(1, gt=0), page_size: int = Query(10, gt=0), db: Session = Depends(get_db)):
    """Endpoint para obtener una lista paginada de productos."""
    result = get_paginated_products(db, page=page, page_size=page_size)
    total_paginas = result['total_pages']
    return {"productos": result['products'], "total_productos": result['total_products'], "total_paginas": total_paginas}

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

@productos.post("/alta_productos", response_model=ProductoResponse, status_code=status.HTTP_201_CREATED)
def create_product(producto: ProductoCreate, db: Session = Depends(get_db)):
    response, status_code = create_product_db(db=db, producto=producto)
    if status_code != 201:
        raise HTTPException(status_code=status_code, detail=response["error"])
    return response["product"]

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