from fastapi import APIRouter, HTTPException, Depends
from models.user_mod import *
from controllers.user_ctl import *
from models.database import get_db
from sqlalchemy.orm import Session

users = APIRouter()

@users.get("/users")
async def busqueda_users(db: Session = Depends(get_db)):
    users = db.query(Usuario).all()
    return users

@users.get("/user/{usr_id}")
async def busqueda_usr_id(usr_id: int, db: Session = Depends(get_db)):
    usr_id = busqueda_user(usr_id, db)
    if usr_id is None:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return usr_id

@users.get("/user/{nombre}")
async def buscar_usr_nombre(nombre: str, db: Session = Depends(get_db)):
    user_encontrado = buscar_usr_nombre(db, nombre)
    if user_encontrado is not None:
        return user_encontrado
    else:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

@users.post("/alta_users", response_model=UserCreate)
async def create_user(usuario: UserCreate, db: Session = Depends(get_db)):
    return create_user_db(db, **usuario.dict())

@users.put("/mod_user/{id}", response_model=ResultadoActUser)
async def update_user(id: int, user: UserUpdate, db: Session = Depends(get_db)):
    usr_existe = busqueda_users(id, db)
    if usr_existe is None:
        raise HTTPException(status_code=404, detail="Usuario no encontrado.")
    
    modificacion = update_user_db(db, id, **user.dict())
    if modificacion:
        return ResultadoActUser(message="Información actualizada correctamente.")
    else:
        raise HTTPException(status_code=404, detail="No se pudo actualizar el producto")