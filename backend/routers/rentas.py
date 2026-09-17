from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import psycopg2
from database import obtener_conexion
from typing import List

router = APIRouter(prefix="/rentas", tags=["Rentas"])

class RentaNueva(BaseModel):
    id_cliente: int
    duracion_pagada: str
    bicicletas: List[int]
class CerrarRenta(BaseModel):
    duracion_real: str
@router.post("")
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
            cursor.execute("SELECT estado FROM bicicletas WHERE id_bici = %s", (id_bici,))
            resultado = cursor.fetchone()
    
            if resultado is None:
                conexion.rollback()
                raise HTTPException(status_code=404, detail=f"La bicicleta {id_bici} no existe")
    
            estado_actual = resultado[0]
            if estado_actual == "En uso":
                conexion.rollback()
                raise HTTPException(status_code=400, detail=f"La bicicleta {id_bici} ya está en uso")
    
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

   

@router.put("/{id_renta}/cerrar")
def cerrar_renta(id_renta: int, datos: CerrarRenta ):
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    try:
        cursor.execute(
            "UPDATE rentas SET duracion_real = %s WHERE id_renta = %s",
            (datos.duracion_real, id_renta)
        )
        conexion.commit()
    finally:
        cursor.close()
        conexion.close()

    return {"mensaje": "Renta cerrada con éxito"}