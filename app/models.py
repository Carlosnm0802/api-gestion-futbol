from .database import Base
from sqlalchemy import Column, Integer, String, Boolean, Date, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime

class Temporada(Base):
    __tablename__ = "temporadas"
    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, index=True)
    fecha_inicio = Column(Date)
    fecha_fin = Column(Date)
    es_actual = Column(Boolean, default=True)
    
    # Relaciones
    equipos = relationship("Equipo", back_populates="temporada")
    partidos = relationship("Partido", back_populates="temporada")

class Categoria(Base):
    __tablename__ = "categorias"
    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, unique=True, index=True)
    
    equipos = relationship("Equipo", back_populates="categoria")

class Equipo(Base):
    __tablename__ = "equipos"
    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, index=True)
    logo_url = Column(String, nullable=True)
    categoria_id = Column(Integer, ForeignKey("categorias.id"))
    temporada_id = Column(Integer, ForeignKey("temporadas.id"))

    # Relaciones
    categoria = relationship("Categoria", back_populates="equipos")
    temporada = relationship("Temporada", back_populates="equipos")
    jugadores = relationship("Jugador", back_populates="equipo")

class Jugador(Base):
    __tablename__ = "jugadores"
    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String)
    apellido = Column(String)
    num_camiseta = Column(Integer)
    posicion = Column(String)
    fecha_nacimiento = Column(Date)
    es_active = Column(Boolean, default=True)
    equipo_id = Column(Integer, ForeignKey("equipos.id"))

    # Relaciones
    equipo = relationship("Equipo", back_populates="jugadores")
    goles = relationship("Gol", back_populates="jugador")

class Partido(Base):
    __tablename__ = "partidos"
    id = Column(Integer, primary_key=True, index=True)
    equipo_local_id = Column(Integer, ForeignKey("equipos.id"))
    equipo_visita_id = Column(Integer, ForeignKey("equipos.id"))
    fecha_partido = Column(DateTime, default=datetime.utcnow)
    goles_local = Column(Integer, default=0)
    goles_visita = Column(Integer, default=0)
    finalizado = Column(Boolean, default=False)
    arbitro = Column(String, nullable=True)
    temporada_id = Column(Integer, ForeignKey("temporadas.id"))

    # Relaciones
    temporada = relationship("Temporada", back_populates="partidos")
    eventos_goles = relationship("Gol", back_populates="partido")

class Gol(Base):
    __tablename__ = "goles"
    id = Column(Integer, primary_key=True, index=True)
    partido_id = Column(Integer, ForeignKey("partidos.id"))
    jugador_id = Column(Integer, ForeignKey("jugadores.id"))
    minuto = Column(Integer)
    es_penalti = Column(Boolean, default=False)

    # Relaciones
    partido = relationship("Partido", back_populates="eventos_goles")
    jugador = relationship("Jugador", back_populates="goles")