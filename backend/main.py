import psycopg2
from dotenv import load_dotenv
import os

load_dotenv()
from fastapi import FastAPI

app = FastAPI()

def obtener_conexion():
    return psycopg2.connect(
        host="localhost",
        database="bicicletas_practica",
        user="postgres",
        password=os.getenv("DB_PASSWORD")
    )
@app.get("/")

def inicio():
    return {"mensaje": "Hola, funciona"}

@app.get("/bicicletas/{id_bici}")

def obtener_bici(id_bici: int):
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    cursor.execute("SELECT id_bici, tipo, contador_uso, estado FROM bicicletas WHERE id_bici = %s", (id_bici,))
    resultado = cursor.fetchone()
    cursor.close()
    conexion.close()

    if resultado is None:
        return {"error": "Bicicleta no encontrada"}

    return {
        "id_bici": resultado[0],
        "tipo": resultado[1],
        "contador_uso": resultado[2],
        "estado": resultado[3]
    }




