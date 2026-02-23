import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

load_dotenv()
load_dotenv()
SQLALCHEMY_DATABASE_URL = os.getenv("DATABASE_URL")  # Asegúrate de que esta variable de entorno esté configurada correctamente
# 2. Creamos el motor con pool_pre_ping para evitar desconexiones en la nube
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, 
    pool_pre_ping=True
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Dependencia para la DB
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()