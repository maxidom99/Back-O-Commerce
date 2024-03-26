from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from pydantic import BaseModel
from typing import Optional

Base = declarative_base()

class Categoria(Base):
    __tablename__ = "categoria"
    id_cat = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String(255), nullable=False)
    baja = Column(String(1), nullable=False, default="N")
    
class CategoryCreate(BaseModel):
    nombre: str
    baja: Optional[str] = None

class CategoryUpdate(BaseModel):
    nombre: Optional[str] = None
    baja: Optional[str] = None
    
class ResultadoActCat(BaseModel):
    message: str