OcoGol API - Sistema de Gestión de Ligas de Fútbol
OcoGol es una API REST profesional diseñada para la gestión integral de torneos de fútbol locales en Ocotlán, Jalisco. El sistema permite administrar temporadas, equipos, plantillas de jugadores y generar estadísticas en tiempo real como la tabla de posiciones.

Stack Tecnológico
Lenguaje: Python 3.10+

Framework: FastAPI (Alto rendimiento y validación automática)

ORM: SQLAlchemy (Mapeo objeto-relacional)

Base de Datos: PostgreSQL hospedado en Supabase

Validación: Pydantic (Modelos de datos y esquemas)

Seguridad: Python-dotenv (Gestión de variables de entorno)

Arquitectura del Proyecto
El proyecto sigue una Arquitectura en Capas para garantizar la escalabilidad y el mantenimiento:

database.py: Configuración del motor de base de datos y gestión de sesiones con Supabase.

models.py: Definición de la estructura de las tablas en PostgreSQL (Capa de Datos).

schemas.py: Contratos de datos y validaciones de entrada/salida (Capa de Validación).

crud.py: Lógica de negocio y consultas a la base de datos (Capa de Servicio).

main.py: Definición de rutas (endpoints) y orquestación del sistema.

Modelo Entidad-Relación (E-R)
El sistema se basa en una estructura relacional sólida que incluye:

Temporadas: El marco temporal de cada torneo.

Categorías: Clasificación de los equipos (Femenil, Veteranos, etc.).

Equipos: Vinculados a una temporada y categoría.

Jugadores: Integrantes de los equipos con estadísticas individuales.

Partidos: Registro de encuentros con marcador automático.

Goles y Sanciones: Eventos en tiempo real que afectan directamente el resultado del partido y la tabla.

Funcionalidades Implementadas
1. Gestión de Datos Maestros
Registro y consulta de temporadas, categorías, equipos y jugadores.

Data Nesting: Las respuestas de la API incluyen información detallada (ej. al consultar un partido, se obtienen los nombres de los equipos, no solo sus IDs).

2. Lógica Automática de Marcadores
Cálculo en Tiempo Real: Al registrar un gol a través del endpoint /goles/, el sistema identifica automáticamente si el jugador pertenece al equipo local o visitante y actualiza el marcador en la tabla de partidos de forma instantánea.

3. Motor de Estadísticas (Día 8)
Tabla de Posiciones Dinámica: Algoritmo que procesa todos los partidos finalizados para calcular:

Puntos (3 por victoria, 1 por empate).

Goles a favor, en contra y diferencia de goles.

Ordenamiento automático bajo criterios de desempate profesionales.

Configuración y Seguridad
El proyecto utiliza un archivo .env para proteger las credenciales de acceso a la base de datos en Supabase, evitando la exposición de información sensible en repositorios públicos.

Bash
# Instalación de dependencias
pip install -r requirements.txt

# Ejecución del servidor
uvicorn app.main:app --reload

Estado del Proyecto y Roadmap
Este proyecto se divide en fases de desarrollo incremental. Actualmente, nos encontramos al inicio de la Fase 4.

 Fase 1: Cimientos y Arquitectura (Completado)
Configuración del Entorno: Creación de entorno virtual y gestión de dependencias (requirements.txt).

Conexión Cloud: Vinculación exitosa con Supabase (PostgreSQL).

Seguridad Inicial: Implementación de variables de entorno (.env) para proteger credenciales.

Boilerplate FastAPI: Estructura de carpetas profesional (Models, Schemas, CRUD, Main).

 Fase 2: Modelado Relacional (Completado)
Diseño E-R: Creación de tablas para Temporadas, Categorías, Equipos y Jugadores.

Esquemas Pydantic: Definición de contratos de datos con Data Nesting para respuestas detalladas.

CRUD Base: Endpoints funcionales para crear y listar la estructura básica de la liga.

 Fase 3: Lógica de Negocio y Eventos (Completado)
Gestión de Partidos: Registro de encuentros vinculados a equipos y temporadas.

Marcador Automático: Desarrollo de lógica en crud.py que actualiza los goles del partido al registrar un evento de gol.

Validación de Sanciones: Sistema que impide sancionar jugadores que no pertenecen al partido en cuestión.

 Fase 4: Analítica y Estadísticas (En Proceso - Día 8)
Tabla de Posiciones: Algoritmo de cálculo en tiempo real (Puntos, GF, GC, DG).

Criterios de Desempate: Ordenamiento lógico basado en reglamento profesional.

Endpoint de Estadísticas: Consulta de clasificación por temporada.

 Futuras Implementaciones (Roadmap)
Fase 5 (Seguridad): Autenticación JWT y roles (Admin/Capitán).

Fase 6 (Multimedia): Subida de logos y fotos a Supabase Storage.

Fase 7 (Frontend): Desarrollo de interfaz móvil/web para los jugadores de Ocotlán.