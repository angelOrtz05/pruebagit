# ============================================================
# Backend de práctica: Renta de Bicicletas
# FastAPI + PostgreSQL (psycopg2)
# ============================================================

# ============================================================
# Backend de práctica: Renta de Bicicletas
# FastAPI + PostgreSQL (psycopg2)
# ============================================================

# ---- Imports estándar de Python ----

from fastapi import FastAPI
from routers import bicicletas, rentas

app = FastAPI(title="API de Renta de Bicicletas")

app.include_router(bicicletas.router)
app.include_router(rentas.router)


@app.get("/")
def inicio():
    return {"mensaje": "Hola, funciona"}
