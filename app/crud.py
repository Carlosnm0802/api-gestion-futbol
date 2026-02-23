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