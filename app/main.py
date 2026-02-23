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

# --- RUTAS DE CATEGORIAS ---

@app.post("/categorias/", response_model=schemas.Categoria, tags=["Categorías"])
def crear_categoria(categoria: schemas.CategoriaCreate, db: Session = Depends(get_db)):
    """Crea una categoría. Es el primer paso antes de registrar equipos."""
    return crud.create_categoria(db=db, categoria=categoria)

@app.get("/categorias/", response_model=List[schemas.Categoria], tags=["Categorías"])
def listar_categorias(db: Session = Depends(get_db)):
    return crud.get_categorias(db)

#RUTAS DE EQUIPOS

@app.post("/equipos/", response_model=schemas.Equipo, tags=["Equipos"])
def crear_equipo(equipo: schemas.EquipoCreate, db: Session = Depends(get_db)):
    """Registra un equipo. Requiere categoria_id y temporada_id existentes."""
    return crud.create_equipo(db=db, equipo=equipo)

@app.get("/equipos/", response_model=List[schemas.Equipo], tags=["Equipos"])
def listar_equipos(db: Session = Depends(get_db)):
    return crud.get_equipos(db)
@app.get("/equipos/{equipo_id}", response_model=schemas.Equipo, tags=["Equipos"])
@app.get("/equipos/{equipo_id}", response_model=schemas.Equipo, tags=["Equipos"])
def leer_equipo(equipo_id: int, db: Session = Depends(get_db)):
    db_equipo = crud.get_equipo_por_id(db, equipo_id=equipo_id)
    if not db_equipo:
        raise HTTPException(status_code=404, detail="Equipo no encontrado")
    return db_equipo
    return db.query(models.Equipo).filter(models.Equipo.id == equipo_id).first()
#RUTAS DE JUGADORES

@app.post("/jugadores/", response_model=schemas.Jugador, tags=["Jugadores"])
def registrar_jugador(jugador: schemas.JugadorCreate, db: Session = Depends(get_db)):
    """Registra un jugador. Requiere un equipo_id válido."""
    return crud.create_jugador(db=db, jugador=jugador)

@app.get("/equipos/{equipo_id}/jugadores", response_model=List[schemas.Jugador], tags=["Jugadores"])
def listar_jugadores_equipo(equipo_id: int, db: Session = Depends(get_db)):
    return crud.get_jugador_por_equipo(db, equipo_id=equipo_id)

@app.get("/jugadores/{jugador_id}", response_model=schemas.Jugador, tags=["Jugadores"])
def leer_jugador(jugador_id: int, db: Session = Depends(get_db)):
    db_jugador = crud.get_jugador_por_id(db, jugador_id=jugador_id)
    if not db_jugador:
        raise HTTPException(status_code=404, detail="Jugador no encontrado")
    return db_jugador