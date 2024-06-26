from fastapi import FastAPI
#from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
#from decouple import config

from controllers.producto_ctl import *
from rutas.productos import *
from rutas.categorias import *
from rutas.users import *
from rutas.descuentos import *

app = FastAPI()

origins = [
    "*"
    ]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configurar el enrutamiento para los archivos estáticos desde la carpeta "static"
#app.mount("/static", StaticFiles(directory="../o-commerce/build/static"), name="static")

app.include_router(productos)
app.include_router(categorias)
app.include_router(users)
app.include_router(descuentos)