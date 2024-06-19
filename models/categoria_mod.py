from sqlalchemy import Column, Integer, String, LargeBinary
from sqlalchemy.ext.declarative import declarative_base
from pydantic import BaseModel
from typing import Optional

Base = declarative_base()

class Categoria(Base):
    __tablename__ = "categoria"
    id_cat = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String(255), nullable=False)
    baja = Column(String(1), nullable=False, default="N")
    img_category = Column(LargeBinary)
    
class CategoryCreate(BaseModel):
    nombre: str
    baja: Optional[str] = "N"
    img_category: Optional[bytes] = None
    
class CategoryResponse(BaseModel):
    id_cat: int
    nombre: str
    baja: Optional[str] = None
    img_category: Optional[bytes] = None

class CategoryUpdate(BaseModel):
    nombre: Optional[str] = None
    baja: Optional[str] = None
    img_category: Optional[bytes] = None

class ResultadoActCat(BaseModel):
    message: str