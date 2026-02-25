from sqlalchemy.orm import Session
from . import models, schemas
from fastapi import HTTPException

#FUNCIONES PARA TEMPORADAS
def get_temporada(db: Session, temporada_id: int):
    return db.query(models.Temporada).filter(models.Temporada.id == temporada_id).first()

def get_temporadas(db: Session, skip: int = 0, limit: int = 100):
    #Obtiene una lista de temporadas con paginación
    return db.query(models.Temporada).offset(skip).limit(limit).all()

def create_temporada(db: Session, temporada: schemas.TemporadaCreate):
    #Crea una nueva temporada en la base de datos
    db_temporada = models.Temporada(
        nombre=temporada.nombre,
        fecha_inicio=temporada.fecha_inicio,
        fecha_fin=temporada.fecha_fin,
        es_actual=temporada.es_actual
    )
    db.add(db_temporada) # Agrega el objeto
    db.commit()          # Guarda los cambios
    db.refresh(db_temporada) # Actualiza el objeto con el ID generado
    return db_temporada
#FUNCIONES PARA CATEGORIAS
def get_categoria(db: Session, categoria_id: int):
    return db.query(models.Categoria).filter(models.Categoria.id == categoria_id).first()

def get_categorias(db: Session, skip: int = 0, limit: int = 100):
    """Obtiene la lista de todas las categorías registradas."""
    return db.query(models.Categoria).offset(skip).limit(limit).all()

def create_categoria(db: Session, categoria: schemas.CategoriaCreate):
    """Crea una nueva categoría (Ej: 'Primera Fuerza')."""
    db_categoria = models.Categoria(nombre=categoria.nombre)
    db.add(db_categoria)
    db.commit()
    db.refresh(db_categoria)
    return db_categoria

#FUNCIONES PARA EQUIPOS
def get_equipo(db: Session, equipo_id: int):
    return db.query(models.Equipo).filter(models.Equipo.id == equipo_id).first()

def get_equipos(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Equipo).offset(skip).limit(limit).all()

def create_equipo(db: Session, equipo: schemas.EquipoCreate):
    db_equipo = models. Equipo( **equipo.model_dump())# Usamos model_dump para mapear los campos
    db.add(db_equipo)
    db.commit()
    db.refresh(db_equipo)
    return db_equipo

#FUNCIONES PARA JUGADORES
def get_jugador(db: Session, jugador_id: int):
    return db.query(models.Jugador).filter(models.Jugador.id == jugador_id).first()

def get_jugador_por_equipo(db: Session, equipo_id: int):
    return db.query(models.Jugador).filter(models.Jugador.equipo_id == equipo_id).all()

def create_jugador(db: Session, jugador: schemas.JugadorCreate):
    db_jugador = models.Jugador(**jugador.model_dump())
    db.add(db_jugador)
    db.commit()
    db.refresh(db_jugador)
    return db_jugador

#FUNCIONES PARA PARTIDOS
def create_partido(db: Session, partido: schemas.PartidoCreate):
    #Crea un partido en la base de datos
    db_partido = models.Partido(**partido.model_dump())
    db.add(db_partido)
    db.commit()
    db.refresh(db_partido)
    return db_partido

def get_partidos(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Partido).offset(skip).limit(limit).all()

#LOGICA DE GOLES PARA ACTUALIZAR PARTIDOS
def registrar_gol(db: Session, gol_data: schemas.GolCreate):
    # 1. Crear el registro del gol
    db_gol = models.Gol(**gol_data.model_dump())
    
    # 2. Buscar el partido para actualizar el marcador
    partido = db.query(models.Partido).filter(models.Partido.id == gol_data.partido_id).first()
    if not partido:
        raise HTTPException(status_code=404, detail="Partido no encontrado")
    
    # 3. Buscar al jugador para saber de qué equipo es
    jugador = db.query(models.Jugador).filter(models.Jugador.id == gol_data.jugador_id).first()
    
    # 4. Lógica de actualización: ¿Es local o visitante?
    if jugador.equipo_id == partido.equipo_local_id:
        partido.goles_local += 1
    elif jugador.equipo_id == partido.equipo_visita_id:
        partido.goles_visita += 1
    else:
        raise HTTPException(status_code=400, detail="El jugador no pertenece a ninguno de los equipos del partido")
    
    db.add(db_gol)
    db.commit()
    db.refresh(db_gol)
    return db_gol

# --- GESTIÓN DE SANCIONES (TARJETAS) ---

def registrar_sancion(db: Session, sancion_data: schemas.SancionCreate):
    # 1. Verificar que el partido exista
    partido = db.query(models.Partido).filter(models.Partido.id == sancion_data.partido_id).first()
    if not partido:
        raise HTTPException(status_code=404, detail="Partido no encontrado")
        
    # 2. Verificar que el jugador pertenezca a alguno de los dos equipos
    jugador = db.query(models.Jugador).filter(models.Jugador.id == sancion_data.jugador_id).first()
    if jugador.equipo_id not in [partido.equipo_local_id, partido.equipo_visita_id]:
        raise HTTPException(
            status_code=400, 
            detail="El jugador no pertenece a los equipos que disputan este partido"
        )
        
    # 3. Crear la sanción
    db_sancion = models.Sancion(**sancion_data.model_dump())
    db.add(db_sancion)
    db.commit()
    db.refresh(db_sancion)
    return db_sancion