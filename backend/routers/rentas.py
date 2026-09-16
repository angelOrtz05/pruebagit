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