from pydantic import BaseModel, ConfigDict
from datetime import date, datetime
from typing import Optional, List
#BASE CONFIG
class BaseSchema(BaseModel):
    model_config=ConfigDict(from_attributes=True)
    #Esto permite que Pydantic lea los datos de SQLAlchemy
#TEMPORADAS
class TemporadaBase(BaseModel):
    nombre: str
    fecha_inicio: date
    fecha_fin:date
    es_actual: bool = True

class TemporadaCreate(TemporadaBase):
    pass #Los datos que pediremos al crear una temporada

class Temporada(TemporadaBase,BaseSchema):
    id: int

#CATEGORIAS
class CategoriaBase(BaseModel):
    nombre: str
class CategoriaCreate(CategoriaBase):
    pass
class Categoria(CategoriaBase,BaseSchema):
    id: int

#EQUIPOS
class EquiposBase(BaseModel):
    nombre: str
    logo_url: Optional[str]=None
    categoria_id: int
    temporada_id: int
class EquipoCreate(EquiposBase):
    pass
class Equipo(EquiposBase,BaseSchema):
    id: int
#JUGADORES
class JugadorBase(BaseModel):
    nombre: str
    apellido: str
    num_camiseta: int
    posicion: str
    fecha_nacimiento: date
    es_activo: bool = True
    equipo_id: int
class JugadorCreate(JugadorBase):
    pass
class Jugador(JugadorBase,BaseSchema):
    id: int
#PARTIDOS
class PartidoBase(BaseModel):
    equipo_local_id: int
    equipo_visita_id: int
    fecha_partido: Optional[datetime]= None
    goles_local: int = 0
    goles_visita: int = 0
    finalizado: bool = False
    arbitro: Optional[str] = None
    temporada_id: int
class PartidoCreate(PartidoBase):
    pass
class Partido(PartidoBase,BaseSchema):
    id: int
#GOLES
class GolBase(BaseModel):
    partido_id: int
    jugador_id: int
    minuto: int
    es_penalti: bool = False
class GolCreate(GolBase):
    pass
class Gol(GolBase,BaseSchema):
    id: int
#SANCIONES
class SancionBase(BaseModel):
    partido_id: int
    jugador_id: int
    tipo: str # "amarilla" o "roja"
class SancionCreate(SancionBase):
    pass
class Sancion(SancionBase,BaseSchema):
    id: int

# ESQUEMAS PARA RESPUESTAS DETALLADAS

class JugadorDetalle(Jugador):
    # Esto traerá la información básica del equipo en lugar de solo el ID
    equipo: Optional[Equipo] = None

class EquipoDetalle(Equipo):
    # Al consultar un equipo, veremos su categoría y temporada completa
    categoria: Optional[Categoria] = None
    temporada: Optional[Temporada] = None
    # Incluso podríamos traer la lista de sus jugadores
    jugadores: List[Jugador] = []

class PartidoDetalle(Partido):
    # Aquí es donde ocurre la magia para la tabla de posiciones
    equipo_local: Optional[Equipo] = None
    equipo_visitante: Optional[Equipo] = None
    temporada: Optional[Temporada] = None