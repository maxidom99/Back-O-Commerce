from sqlalchemy import Column, Integer, String, Float
from sqlalchemy.ext.declarative import declarative_base
from pydantic import BaseModel
from typing import Optional

Base = declarative_base()

class Descuento(Base):
    __tablename__ = "descuentos"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    nombre = Column(String(255) ,index=True)
    descripcion = Column(String(255))
    baja = Column(String(1), nullable=False, default="N")

class DescuentoCreate(BaseModel):
    nombre: str
    descripcion: str
    baja: Optional[str] = None
    
class DescuentoUpdate(BaseModel):
    nombre: Optional[str] = None
    descripcion: Optional[str] = None
    baja: Optional[str] = None
    
class ResultadoActDsc(BaseModel):
    message: str