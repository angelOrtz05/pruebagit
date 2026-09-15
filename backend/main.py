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

from pydantic import BaseModel
from typing import List

class RentaNueva(BaseModel):
    id_cliente: int
    duracion_pagada: str
    bicicletas: List[int]

@app.post("/rentas")
def crear_renta(renta: RentaNueva):
    conexion = obtener_conexion()         # función que ya escribiste antes
    cursor = conexion.cursor()     # cómo abrías un cursor

    # 1. Insertar en `rentas`, y pedir que te devuelva el id_renta generado
    cursor.execute(
        "INSERT INTO rentas (id_cliente, duracion_pagada) VALUES (%s, %s) RETURNING id_renta",
        (renta.id_cliente, renta.duracion_pagada)   # ¿de dónde sacas estos dos valores? (pista: vienen del objeto `renta`)
    )
    id_renta = cursor.fetchone()[0]   # ¿qué función lees UNA fila de resultado?

    # 2. Insertar una fila en `cuenta` por cada bici de la lista
    for elemento in renta.bicicletas:     # nombra la variable del ciclo
        cursor.execute(
            "INSERT INTO cuenta (id_renta, id_bici) VALUES (%s, %s)",
            (id_renta,elemento)
        )

    # 3. Guardar los cambios de forma permanente
    conexion.commit()

    # 4. Cerrar cursor y conexión
    cursor.close()
    conexion.close()

    # 5. Regresar una confirmación (puedes incluir el id_renta generado)
    return {"mensaje": "Se creo con exito la nueva renta: ",
            "ID Renta: ": id_renta}

@app.put("/bicicletas/{id_bici}")
def aumentar_contador(id_bici: int):
    conexion = obtener_conexion()
    cursor = conexion.cursor()

    cursor.execute(
        "UPDATE bicicletas SET contador_uso = contador_uso + 1 WHERE id_bici = %s",
        (id_bici,)
    )
    conexion.commit()
    cursor.close()
    conexion.close()

    return {"Mensaje" : "Contador aumentado con exito"}

@app.delete("/bicicletas/{id_bici}")
def eliminar_bici(id_bici : int):
    conexion= obtener_conexion()
    cursor = conexion.cursor()

    cursor.execute(
        "DELETE FROM bicicletas WHERE id_bici=%s",
        (id_bici,)
    )
    conexion.commit()
    cursor.close()
    conexion.close()

    return{"Mensaje" : "Se elimino correctamente la bicicleta ",
           "id_bici" : id_bici}

class BiciNueva(BaseModel):
    contador_uso: int = 0
    tipo: str
    estado: str = "Disponible"


@app.post("/bicicletas")
def crear_bici(bici: BiciNueva):
    conexion = obtener_conexion()         
    cursor = conexion.cursor()

    cursor.execute(
        "INSERT INTO bicicletas (contador_uso,tipo,estado) VALUES (%s, %s,%s) RETURNING id_bici",
        (bici.contador_uso,bici.tipo,bici.estado)   
    )
    id_bici = cursor.fetchone()[0]  

    # 3. Guardar los cambios de forma permanente
    conexion.commit()

    # 4. Cerrar cursor y conexión
    cursor.close()
    conexion.close()

    # 5. Regresar una confirmación (puedes incluir el id_renta generado)
    return {"mensaje": "Se creo con exito la nueva bici: ",
            "ID Bici: ": id_bici}
