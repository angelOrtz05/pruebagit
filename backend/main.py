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
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI(title="API de Renta de Bicicletas")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(bicicletas.router)
app.include_router(rentas.router)


@app.get("/")
def inicio():
    return {"mensaje": "Hola, funciona"}
