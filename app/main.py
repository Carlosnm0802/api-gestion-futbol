from fastapi import FastAPI
app = FastAPI(
    title="API de Gestion de Futbol Ocotlan",
    description="API para gestionar equipos, jugadores y partidos de futbol en Ocotlan.",
    version="1.0.0"
)
@app.get("/")
def root():
    return {"message": "Bienvenido a la API de Gestión de Futbol Ocotlan",
            "estado": "Servidor funcionando correctamente"}

