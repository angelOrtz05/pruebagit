import os

# ---- Imports de librerías externas ----
import psycopg2
from dotenv import load_dotenv

# ---- Carga de variables de entorno (.env) ----
load_dotenv()

# ============================================================
# CONEXIÓN A LA BASE DE DATOS
# ============================================================

def obtener_conexion():
    """Abre y regresa una nueva conexión a PostgreSQL."""
    return psycopg2.connect(
        host="localhost",
        database="bicicletas_practica",
        user="postgres",
        password=os.getenv("DB_PASSWORD")
    )
