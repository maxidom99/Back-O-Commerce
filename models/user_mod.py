from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from pydantic import BaseModel
from typing import Optional

Base = declarative_base()

class Usuario(Base):
    __tablename__ = "usuarios"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    documento = Column(String(15), index=True)
    nombre = Column(String(255) ,index=True)
    apellido = Column(String(255))
    e_mail = Column(String(255))
    contrasenia = Column(String(40))
    baja = Column(String(1), nullable=False, default="N")
    img_perfil = Column(String(255))
    rol = Column(String(1), nullable=False, default="C")

class UserCreate(BaseModel):
    documento: str
    nombre: str
    apellido: str
    e_mail: str
    contrasenia: str
    baja: Optional[str] = None
    img_perfil: Optional[str] = None
    rol: Optional[str] = "C"
    
class UserUpdate(BaseModel):
    contrasenia: Optional[str] = None
    baja: Optional[str] = None
    e_mail: Optional[str] = None
    img_perfil: Optional[str] = None
    
class ResultadoActUser(BaseModel):
    message: str