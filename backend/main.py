# ============================================================
# Backend de práctica: Renta de Bicicletas
# FastAPI + PostgreSQL (psycopg2)
# ============================================================

# ---- Imports estándar de Python ----
import os

# ---- Imports de librerías externas ----
import psycopg2
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List

# ---- Carga de variables de entorno (.env) ----
load_dotenv()

# ---- Instancia principal de la app ----
app = FastAPI(title="API de Renta de Bicicletas")


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


# ============================================================
# MODELOS (Pydantic) — la "forma" de los datos que se reciben
# ============================================================

class RentaNueva(BaseModel):
    id_cliente: int
    duracion_pagada: str
    bicicletas: List[int]


class BiciNueva(BaseModel):
    tipo: str
    contador_uso: int = 0
    estado: str = "Disponible"


# ============================================================
# RUTAS — RAÍZ
# ============================================================

@app.get("/")
def inicio():
    return {"mensaje": "Hola, funciona"}


# ============================================================
# RUTAS — BICICLETAS
# ============================================================

@app.get("/bicicletas/{id_bici}")
def obtener_bici(id_bici: int):
    """Devuelve los datos de una bicicleta específica por su ID."""
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    try:
        cursor.execute(
            "SELECT id_bici, tipo, contador_uso, estado "
            "FROM bicicletas WHERE id_bici = %s",
            (id_bici,)
        )
        resultado = cursor.fetchone()
    finally:
        cursor.close()
        conexion.close()

    if resultado is None:
        raise HTTPException(status_code=404, detail="Bicicleta no encontrada")

    return {
        "id_bici": resultado[0],
        "tipo": resultado[1],
        "contador_uso": resultado[2],
        "estado": resultado[3]
    }


@app.post("/bicicletas")
def crear_bici(bici: BiciNueva):
    """Registra una bicicleta nueva en el inventario."""
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    try:
        cursor.execute(
            "INSERT INTO bicicletas (contador_uso, tipo, estado) "
            "VALUES (%s, %s, %s) RETURNING id_bici",
            (bici.contador_uso, bici.tipo, bici.estado)
        )
        id_bici = cursor.fetchone()[0]
        conexion.commit()
    finally:
        cursor.close()
        conexion.close()

    return {"mensaje": "Se creó con éxito la nueva bici", "id_bici": id_bici}


@app.put("/bicicletas/{id_bici}/incrementar-uso")
def aumentar_contador(id_bici: int):
    """Suma 1 al contador de uso de una bicicleta."""
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    try:
        cursor.execute(
            "UPDATE bicicletas SET contador_uso = contador_uso + 1 "
            "WHERE id_bici = %s",
            (id_bici,)
        )
        conexion.commit()
    finally:
        cursor.close()
        conexion.close()

    return {"mensaje": "Contador aumentado con éxito"}


@app.delete("/bicicletas/{id_bici}")
def eliminar_bici(id_bici: int):
    """Elimina una bicicleta, si no tiene registros relacionados."""
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    try:
        cursor.execute("DELETE FROM bicicletas WHERE id_bici = %s", (id_bici,))
        conexion.commit()
    except psycopg2.Error:
        conexion.rollback()
        raise HTTPException(
            status_code=409,
            detail="No se puede eliminar: la bicicleta tiene registros relacionados"
        )
    finally:
        cursor.close()
        conexion.close()

    return {"mensaje": "Bicicleta eliminada con éxito"}


# ============================================================
# RUTAS — RENTAS
# ============================================================

@app.post("/rentas")
def crear_renta(renta: RentaNueva):
    """Crea una renta nueva y la asocia a una o varias bicicletas."""
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    try:
        cursor.execute(
            "INSERT INTO rentas (id_cliente, duracion_pagada) "
            "VALUES (%s, %s) RETURNING id_renta",
            (renta.id_cliente, renta.duracion_pagada)
        )
        id_renta = cursor.fetchone()[0]

        for id_bici in renta.bicicletas:
            cursor.execute(
                "INSERT INTO cuenta (id_renta, id_bici) VALUES (%s, %s)",
                (id_renta, id_bici)
            )

        conexion.commit()
    except psycopg2.Error:
        conexion.rollback()
        raise HTTPException(status_code=400, detail="No se pudo crear la renta")
    finally:
        cursor.close()
        conexion.close()

    return {"mensaje": "Se creó con éxito la nueva renta", "id_renta": id_renta}