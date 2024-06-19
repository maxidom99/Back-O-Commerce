from fastapi import APIRouter, HTTPException, Depends, Body, status
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

@users.post("/alta_users", response_model=dict, status_code=status.HTTP_201_CREATED)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    response, status_code = create_user_db(db, user)
    if status_code != 201:
        raise HTTPException(status_code=status_code, detail=response["error"])
    return response

@users.put("/mod_user/{id}", response_model=ResultadoActUser)
async def update_user(id: int, user: UserUpdate, db: Session = Depends(get_db)):
    usr_existe = busqueda_usr_id(id, db)
    if usr_existe is None:
        raise HTTPException(status_code=404, detail="Usuario no encontrado.")
    
    updated_user, message = update_user_db(db, id, **user.dict())
    if updated_user:
        return ResultadoActUser(message=message)
    else:
        raise HTTPException(status_code=404, detail=message)

@users.post("/login")
def login_usr(db: Session = Depends(get_db), login_data: dict = Body(...)):
    e_mail = login_data.get("e_mail")
    contrasenia = login_data.get("contrasenia")

    if not e_mail or not contrasenia:
        raise HTTPException(status_code=400, detail="Ingrese el email y la contraseña")

    user = LoginController.login(db, e_mail, contrasenia)
    if not user:
        raise HTTPException(status_code=401, detail="Contraseña o email inválido")

    return {user}