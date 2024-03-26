from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from pydantic import BaseModel
from typing import Optional

Base = declarative_base()

class Administrador(Base):
    __tablename__ = "admin"
    id = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String(255), nullable=False)
    apellido = Column(String(255), nullable=False)
    contrasenia = Column(String(60), nullable=False)
    e_mail = Column(String(60))
    baja = Column(String(1), nullable=False, default="N")
    
class AdminCreate(BaseModel):
    nombre: str
    apellido: str
    e_mail: str
    contrasenia: str
    baja: Optional[str] = None

class AdminUpdate(BaseModel):
    nombre: Optional[str] = None
    apellido: Optional[str] = None
    e_mail: Optional[str] = None
    contrasenia: Optional[str] = None
    baja: Optional[str] = None
    
class ResultadoActAdm(BaseModel):
    message: str