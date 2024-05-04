from sqlalchemy import Column, Integer, String, Float, LargeBinary
from sqlalchemy.ext.declarative import declarative_base
from pydantic import BaseModel
from typing import Optional

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

class ProductoCreate(BaseModel):
    precios: float
    nombres: str
    id_cat: int
    baja: Optional[str] = None
    descripcion: str
    img_product: Optional[bytes] = None
    
class ProductoUpdate(BaseModel):
    precios: Optional[float] = None
    nombres: Optional[str] = None
    id_cat: Optional[int] = None
    baja: Optional[str] = None
    descripcion: Optional[str] = None
    img_product: Optional[bytes] = None

class ResultadoAct(BaseModel):
    message: str
