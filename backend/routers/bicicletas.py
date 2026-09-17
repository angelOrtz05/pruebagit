from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import psycopg2
from database import obtener_conexion

router = APIRouter(prefix="/bicicletas", tags=["Bicicletas"])


class BiciNueva(BaseModel):
    tipo: str
    contador_uso: int = 0
    estado: str = "Disponible"


@router.get("/{id_bici}")
def obtener_bici(id_bici: int):
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




@router.post("")
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


@router.put("/{id_bici}/incrementar-uso")
def aumentar_contador(id_bici: int):
    """Suma 1 al contador de uso de una bicicleta."""
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    try:
        cursor.execute(
            "UPDATE bicicletas SET contador_uso = contador_uso + 1 "
            "WHERE id_bici = %s RETURNING contador_uso, estado",
            (id_bici,)
        )
        contador_uso, estado = cursor.fetchone()
        conexion.commit()
    finally:
        cursor.close()
        conexion.close()

    return {"mensaje": "Contador aumentado con éxito",  "contador_uso": contador_uso,
            "estado": estado}


@router.delete("/{id_bici}")
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

    return {"mensaje": "Bicicleta eliminada con éxito", "id_bici": id_bici}
    