from sqlalchemy import Column, Integer, String, Float, LargeBinary, Date
from sqlalchemy.ext.declarative import declarative_base
from pydantic import BaseModel
from typing import Optional
from datetime import date

Base = declarative_base()

class Producto(Base):
    __tablename__ = "productos"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    precios = Column(Float, nullable=False)
    nombres = Column(String(255) ,index=True)
    id_cat = Column(Integer)
    baja = Column(String(1), nullable=False, default="N")
    descripcion = Column(String(1000))
    img_product = Column(LargeBinary)
    
class Ventas(Base):
    __tablename__ = "ventas"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    fecha_venta = Column(Date, nullable=False)
    id_producto = Column(Integer)
    id_usuario = Column(Integer)

class ProductoCreate(BaseModel):
    precios: float
    nombres: str
    id_cat: int
    baja: Optional[str] = "N"
    descripcion: str
    img_product: Optional[bytes] = None
class VentaCreate(BaseModel):
    id_producto: int
    id_usuario: int
    fecha_venta: Optional[date] = None
    
class ProductoResponse(BaseModel):
    id: int
    precios: float
    nombres: str
    id_cat: int
    baja: Optional[str] = "N"
    descripcion: str
    img_product: Optional[bytes] = None

    class Config:
        orm_mode = True
    
class ProductoUpdate(BaseModel):
    precios: Optional[float] = None
    nombres: Optional[str] = None
    id_cat: Optional[int] = None
    baja: Optional[str] = None
    descripcion: Optional[str] = None
    img_product: Optional[bytes] = None
    
class ProductoPurchased(BaseModel):
    id: int
    nombres: Optional[str] = None
    precios: Optional[float] = None
    img_product: Optional[bytes] = None
    
class ResultadoAct(BaseModel):
    message: str
