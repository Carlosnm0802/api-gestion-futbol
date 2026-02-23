from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from . import crud, models, schemas
from .database import engine, get_db

# Crea las tablas en Supabase si no existen
models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="API de Gestión de Fútbol Ocotlán",
    description="Sistema profesional para la gestión de torneos locales.",
    version="1.0.0"
)

#RUTAS DE TEMPORADAS

@app.post("/temporadas/", response_model=schemas.Temporada, tags=["Temporadas"])
def crear_temporada(temporada: schemas.TemporadaCreate, db: Session = Depends(get_db)):
    """
    Crea una nueva temporada (Ej: 'Clausura 2026') en la base de datos de Supabase.
    """
    return crud.create_temporada(db=db, temporada=temporada)

@app.get("/temporadas/", response_model=List[schemas.Temporada], tags=["Temporadas"])
def listar_temporadas(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """
    Obtiene la lista de todas las temporadas registradas.
    """
    temporadas = crud.get_temporadas(db, skip=skip, limit=limit)
    return temporadas
@app.get("/temporadas/{temporada_id}", response_model=schemas.Temporada, tags=["Temporadas"])
def leer_temporada(temporada_id: int, db: Session = Depends(get_db)):
    db_temporada = crud.get_temporada(db, temporada_id=temporada_id)
    if db_temporada is None:
        raise HTTPException(status_code=404, detail="Temporada no encontrada en Ocotlán")
    return db_temporada