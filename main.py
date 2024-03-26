from fastapi import FastAPI
#from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware

from controllers.producto_ctl import *
from rutas.productos import *
from rutas.categorias import *
from rutas.clientes import *
from rutas.descuentos import *
from rutas.administradores import *

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configurar el enrutamiento para los archivos estáticos desde la carpeta "static"
#app.mount("/static", StaticFiles(directory="../o-commerce/build/static"), name="static")

app.include_router(productos)
app.include_router(categorias)
app.include_router(clientes)
app.include_router(descuentos)
app.include_router(administradores)