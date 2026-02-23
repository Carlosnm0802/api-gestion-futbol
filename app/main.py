from fastapi import FastAPI
from .database import engine
from . import models

#Esta linea crea las tablas de la base de datos si no existen, basándose en los modelos definidos en models.py
models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="API de Gestión de Fútbol Ocotlán",
    version="1.0.0"
)

@app.get("/")
def root():
    return {"mensaje": "Conexión con Supabase establecida"}