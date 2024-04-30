from fastapi import APIRouter, HTTPException, Depends
from models.descuento_mod import *
from controllers.descuento_ctl import *
from models.database import get_db
from sqlalchemy.orm import Session

descuentos = APIRouter()

@descuentos.get("/descuentos")
async def busqueda_descuentos(db: Session = Depends(get_db)):
    descuentos = db.query(Descuento).filter(Descuento.baja == 'N').all()
    return descuentos

@descuentos.get("/descuentos/{id}")
async def busqueda_dsc_id(id: int, db: Session = Depends(get_db)):
    dsc_id = busqueda_descuento(id, db)
    if dsc_id is not None:
        return dsc_id
    else:
        raise HTTPException(status_code=404, detail="Descuento no encontrado")
    
@descuentos.get("/discount/{nombre}")
async def buscar_discount_nombre(nombre: str, db: Session = Depends(get_db)):
    descuento_encontrado = buscar_dsc_nombre(db, nombre)
    if descuento_encontrado is not None:
        return descuento_encontrado
    else:
        raise HTTPException(status_code=404, detail="Descuento no encontrado")

@descuentos.post("/alta_descuentos", response_model=DescuentoCreate)
async def create_discount(descuento: DescuentoCreate, db: Session = Depends(get_db)):
    return create_dsc_db(db, **descuento.dict())

@descuentos.put("/mod_discount/{id_dsc}", response_model=ResultadoActDsc)
async def update_discount(id_dsc: int, descuento: DescuentoUpdate, db: Session = Depends(get_db)):
    dsc_existe = busqueda_descuento(id_dsc, db)
    if dsc_existe is None:
        raise HTTPException(status_code=404, detail="Descuento no encontrado.")
    
    modificacion = update_discount_db(db, id_dsc, **descuento.dict())
    if modificacion:
        return ResultadoActDsc(message="Descuento actualizado correctamente.")
    else:
        raise HTTPException(status_code=404, detail="No se pudo actualizar el descuento")