from .auth import get_current_user
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from . import crud, models, schemas
from .database import engine, get_db
from fastapi.security import OAuth2PasswordRequestForm
from .auth import create_access_token, verify_password, ACCESS_TOKEN_EXPIRE_MINUTES
from datetime import timedelta

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
def crear_equipo(
    equipo: schemas.EquipoCreate, 
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    """
    Registra un equipo. REQUIERE TOKEN DE ADMINISTRADOR.
    """
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

# --- RUTAS DE PARTIDOS ---

@app.post("/partidos/", response_model=schemas.Partido, tags=["Partidos"])
def crear_partido(partido: schemas.PartidoCreate, db: Session = Depends(get_db)):
    return crud.create_partido(db=db, partido=partido)

@app.get("/partidos/", response_model=List[schemas.Partido], tags=["Partidos"])
def listar_partidos(db: Session = Depends(get_db)):
    return crud.get_partidos(db)

#RUTAS DE EVENTOS (GOLES Y SANCIONES)

@app.post("/goles/", response_model=schemas.Gol, tags=["Eventos"])
def anotar_gol(gol: schemas.GolCreate, db: Session = Depends(get_db)):
    """Registra un gol y actualiza automáticamente el marcador del partido."""
    return crud.registrar_gol(db=db, gol_data=gol)

@app.post("/sanciones/", response_model=schemas.Sancion, tags=["Eventos"])
def registrar_sancion(sancion: schemas.SancionCreate, db: Session = Depends(get_db)):
    """
    Registra una tarjeta (Amarilla/Roja) validando que el jugador esté en el partido.
    """
    return crud.registrar_sancion(db=db, sancion_data=sancion)

@app.get("/temporadas/{temporada_id}/tabla", response_model=List[schemas.TablaPosiciones], tags=["Estadísticas"])
def obtener_tabla_de_posiciones(temporada_id: int, db: Session = Depends(get_db)):
    """
    Calcula y devuelve la tabla de posiciones en tiempo real para una temporada específica.
    """
    return crud.get_tabla_posiciones(db, temporada_id=temporada_id)

@app.patch("/partidos/{partido_id}/finalizar", response_model=schemas.Partido, tags=["Partidos"])
def finalizar_partido(partido_id: int,db: Session = Depends(get_db)):
    """Marca un partido como finalizado.
    Esto hara que sus goles cuenten oficialmente para la tabla de posiciones."""
    partido = crud.finalizar_partido(db,partido_id=partido_id)
    if not partido:
        raise HTTPException(status_code=404, detail='Partido no encontrado')
    return partido 

@app.post("/users/", response_model=schemas.User, tags=["Seguridad"])
def registrar_usuario(user: schemas.UserCreate, db: Session = Depends(get_db)):
    """
    Crea un nuevo administrador. La contraseña se encripta automáticamente.
    """
    # Verificamos si el nombre de usuario ya existe
    db_user = crud.get_user_by_username(db, username=user.username)
    if db_user:
        raise HTTPException(status_code=400, detail="El nombre de usuario ya está registrado en Ocotlán")
    
    return crud.create_user(db=db, user=user)

@app.post("/token", response_model=schemas.Token, tags=["Seguridad"])
def login_para_obtener_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(), 
    db: Session = Depends(get_db)
):
    # Buscamos al usuario en la base de datos de Ocotlán
    user = crud.get_user_by_username(db, username=form_data.username)
    
    # Validamos si existe y si la contraseña (hash) coincide
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=401,
            detail="Usuario o contraseña incorrectos",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    #Generamos el pase VIP (Token)
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, 
        expires_delta=access_token_expires
    )
    
    return {"access_token": access_token, "token_type": "bearer"}