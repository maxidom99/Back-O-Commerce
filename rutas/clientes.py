from fastapi import APIRouter, HTTPException, Depends
from models.cliente_mod import *
from controllers.cliente_ctl import *
from database import get_db
from sqlalchemy.orm import Session

clientes = APIRouter()

@clientes.get("/clientes")
async def busqueda_clientes(db: Session = Depends(get_db)):
    clientes = db.query(Cliente).all()
    return clientes

@clientes.get("/clientes/{client_id}")
async def busqueda_cli_id(client_id: int, db: Session = Depends(get_db)):
    cli_id = busqueda_cliente(client_id, db)
    if cli_id is None:
        raise HTTPException(status_code=404, detail="Cliente no encontrado")
    return cli_id

@clientes.get("/client/{nombre}")
async def buscar_client_nombre(nombre: str, db: Session = Depends(get_db)):
    cliente_encontrado = buscar_cli_nombre(db, nombre)
    if cliente_encontrado is not None:
        return cliente_encontrado
    else:
        raise HTTPException(status_code=404, detail="Cliente no encontrado")

@clientes.post("/alta_clientes", response_model=ClienteCreate)
async def create_product(cliente: ClienteCreate, db: Session = Depends(get_db)):
    return create_client_db(db, **cliente.dict())

@clientes.put("/mod_cliente/{id}", response_model=ResultadoActCliente)
async def update_client(id: int, cliente: ClienteUpdate, db: Session = Depends(get_db)):
    cli_existe = busqueda_cliente(id, db)
    if cli_existe is None:
        raise HTTPException(status_code=404, detail="Cliente no encontrado.")
    
    modificacion = update_client_db(db, id, **cliente.dict())
    if modificacion:
        return ResultadoActCliente(message="Información actualizada correctamente.")
    else:
        raise HTTPException(status_code=404, detail="No se pudo actualizar el producto")