from fastapi import APIRouter, HTTPException, Depends
from models.administrador_mod import *
from controllers.administrador_ctl import *
from database import get_db
from sqlalchemy.orm import Session

administradores = APIRouter()

@administradores.get("/administradores")
async def busqueda_administradores(db: Session = Depends(get_db)):
    administrador = db.query(Administrador).all()
    return administrador

@administradores.get("/administradores/{admin_id}")
async def busqueda_adm_id(admin_id: int, db: Session = Depends(get_db)):
    adm_id = busqueda_adm(admin_id, db)
    if adm_id is None:
        raise HTTPException(status_code=404, detail="Administrador no encontrado.")
    return adm_id

@administradores.get("/admin/{nombre}")
async def busqueda_adm_nombre(nombre: str, db: Session = Depends(get_db)):
    name_adm = buscar_name_adm(db, nombre)
    if name_adm is not None:
        return name_adm
    else:
        raise HTTPException(status_code=404, detail="Administrador no encontrado.")

@administradores.post("/crear_admin", response_model=AdminCreate)
async def create_admin(admin: AdminCreate, db: Session = Depends(get_db)):
    return create_admin_db(db, **admin.dict())

@administradores.put("/mod_admin/{admin_id}", response_model=ResultadoActAdm)
async def update_admin(admin_id: int, admin: AdminUpdate, db: Session = Depends(get_db)):
    adm_existe = busqueda_adm(admin_id, db)
    if adm_existe is None:
        raise HTTPException(status_code=404, detail="Administrador no encontrado.")
    
    modificacion = update_admin_db(db, admin_id, **admin.dict())
    if modificacion:
        return ResultadoActAdm(message="Administrador actualizado correctamente.")
    else:
        raise HTTPException(status_code=404, detail="No se pudo actualizar el administrador.")