from sqlalchemy.orm import Session
from . import models, schemas

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
