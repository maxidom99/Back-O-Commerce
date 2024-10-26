import mercadopago as mp

from fastapi import APIRouter, HTTPException, Depends, Query, status
from models.producto_mod import *
from controllers.producto_ctl import *
from models.database import get_db
from sqlalchemy.orm import Session

productos = APIRouter()
sdk = mp.SDK("APP_USR-6185876624553497-102612-be1ed5d5e1701dad5647b80780439677-1880004658")

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

@productos.post("/comprar_ahora/{id_producto}/{id_usuario}")
def comprar_ahora(id_producto: int, id_usuario: int, db: Session = Depends(get_db)):
    # Buscar el producto en la base de datos
    producto = db.query(Producto).filter(Producto.id == id_producto).first()
    
    if not producto:
        raise HTTPException(status_code=404, detail="Producto no encontrado")

    # Registrar la intención de compra en la tabla Ventas
    nueva_venta = Ventas(
        fecha_venta=date.today(),
        id_usuario=id_usuario,
        id_producto=id_producto
    )
    
    create_sell_db(db, nueva_venta)

    # Crear la preferencia de pago en Mercado Pago
    preference_data = {
        "items": [
            {
                "id": producto.id,
                "category_id": producto.id_cat,
                "description": producto.descripcion,
                "unit_price": 2200,
                "title": producto.nombres,
                "quantity": 1,
                "unit_price": float(producto.precios),
                "currency_id": "UYU"
            }
        ],
        "back_urls": {
            "success": "https://tu-sitio.com/success",
            "failure": "https://tu-sitio.com/failure",
            "pending": "https://tu-sitio.com/pending"
        },
        "auto_return": "approved"
    }

    # Crear la preferencia utilizando el SDK de Mercado Pago
    preference_response = sdk.preference().create(preference_data)

    # Verificar si la respuesta tiene el campo 'response' y 'init_point'
    if "response" not in preference_response or "init_point" not in preference_response["response"]:
        # Imprimir la respuesta completa para depuración
        print("Error en la respuesta de Mercado Pago:", preference_response)
        raise HTTPException(status_code=400, detail="Error al crear la preferencia de pago")

    return {"init_point": preference_response["response"]['init_point']}

# @productos.post("/webhook")
# async def webhook(data: dict, db: Session = Depends(get_db)):
#     payment_id = data.get("data", {}).get("id")

#     # Consultar el estado del pago en Mercado Pago
#     payment_info = mp.payment().get(payment_id)

#     if payment_info["status"] == 200:
#         # Extraer el estado del pago
#         status = payment_info["response"]["status"]
#         id_producto = payment_info["response"]["additional_info"]["items"][0]["id"]

#         # Actualizar la venta en la base de datos
#         venta = db.query(Ventas).filter(Ventas.id_producto == id_producto).first()
#         if venta:
#             venta.estado = status  # Actualiza el estado de la venta (ej. "approved")
#             db.commit()
    
#     return {"status": "ok"}
    

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