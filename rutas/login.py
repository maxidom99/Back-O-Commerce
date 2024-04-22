# rutas/login.py
from fastapi import APIRouter, Depends, HTTPException, Body
from sqlalchemy.orm import Session
from database import get_db
from controllers.login_ctl import LoginController

login = APIRouter()

@login.post("/login")
def login_usr(db: Session = Depends(get_db), login_data: dict = Body(...)):
    e_mail = login_data.get("e_mail")
    contrasenia = login_data.get("contrasenia")

    if not e_mail or not contrasenia:
        raise HTTPException(status_code=400, detail="Email and password are required")

    user = LoginController.login(db, e_mail, contrasenia)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid email or password")

    return {"message": "Login successful"}