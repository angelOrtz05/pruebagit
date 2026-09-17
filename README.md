# Sistema de Renta de Bicicletas (Proyecto de Práctica)

Proyecto de práctica para aprender modelado de bases de datos, backend con
FastAPI y conexión con un frontend simple, como preparación para el proyecto
real: un sistema de inventario para una clínica de belleza.

## Estado del proyecto

**Completo y funcional** para el caso de uso básico de renta de bicicletas.
No es un producto terminado — es un ejercicio de práctica end-to-end.

## Qué hace

- Modela clientes, bicicletas, rentas y mantenimiento en PostgreSQL.
- Expone una API en FastAPI para crear, consultar, actualizar y eliminar
  bicicletas, y para crear y cerrar rentas.
- Automatiza reglas de negocio con triggers de PostgreSQL:
  - Al rentar una bici, su estado cambia a "En uso" automáticamente.
  - Al cerrar una renta, la bici vuelve a "Disponible" y su contador de uso
    sube en 1.
  - Al registrar un mantenimiento, el contador de uso se reinicia a 0.
- Incluye un frontend mínimo en HTML/JavaScript para probar las rutas
  principales sin depender de `/docs`.

## Qué está completo

- [x] Modelo de datos con 5 tablas y relaciones (uno a muchos, muchos a
      muchos resuelta con tabla intermedia).
- [x] CRUD completo de bicicletas (crear, consultar una, listar todas,
      eliminar).
- [x] Crear y cerrar rentas, incluyendo rentas con varias bicicletas a la
      vez.
- [x] Validación: no se puede rentar una bicicleta que ya está en uso.
- [x] Transacciones: si algo falla a medio camino al crear una renta, no
      queda ningún dato a medias.
- [x] Manejo de errores con códigos HTTP apropiados (404, 400, 409).
- [x] Backend organizado en routers (uno por entidad).
- [x] Conexión de PostgreSQL protegida con variables de entorno (`.env`).
- [x] Frontend básico conectado a la API (consultar, listar, crear renta).

## Qué falta (fuera del alcance de este ejercicio)

- [ ] Autenticación y manejo de usuarios/permisos.
- [ ] Actualizar o editar una bicicleta existente (`PUT` general, más allá
      del incremento de contador que ahora vive solo en el trigger).
- [ ] Frontend para registrar mantenimiento.
- [ ] Paginación en el listado de bicicletas (no urgente a esta escala).
- [ ] Reportes con `GROUP BY` expuestos como rutas de la API (por ahora
      solo existen como consultas sueltas en el `.sql`).
- [ ] Pruebas automatizadas (unit tests).
- [ ] Configuración lista para producción (HTTPS, CORS restringido a un
      dominio específico, usuario de base de datos con permisos limitados).

## Estructura del proyecto

```
DB_Adriana/
├── sql/
│   └── practica_bicicletas.sql   # tablas, triggers, datos y consultas de referencia
├── backend/
│   ├── main.py                   # arranca la app y conecta los routers
│   ├── database.py               # conexión a PostgreSQL
│   ├── requirements.txt          # dependencias de Python
│   ├── .env                      # credenciales (no se sube al repo)
│   └── routers/
│       ├── bicicletas.py
│       └── rentas.py
└── frontend/
    └── index.html                # interfaz mínima para probar la API
```

## Cómo correrlo desde cero

1. Crear una base de datos en PostgreSQL llamada `bicicletas_practica`.
2. Ejecutar el contenido de `sql/practica_bicicletas.sql` en esa base de
   datos (crea las tablas, los triggers y algunos datos de ejemplo).
3. Dentro de `backend/`, crear un archivo `.env` con:
   ```
   DB_PASSWORD=tu_contraseña_de_postgres
   ```
4. Instalar las dependencias:
   ```
   pip install -r requirements.txt
   ```
5. Levantar el servidor:
   ```
   uvicorn main:app --reload
   ```
6. Probar la API en `http://127.0.0.1:8000/docs`, o abrir
   `frontend/index.html` directamente en el navegador.

## Próximos pasos

Este proyecto se pausa aquí. El patrón aprendido (modelo → triggers →
backend con manejo de errores y transacciones → frontend) se va a aplicar
directamente al proyecto real: un sistema de inventario para una clínica
de belleza (productos, lotes con fecha de caducidad, proveedores y
servicios).
