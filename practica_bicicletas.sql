-- ============================================================
-- CASO DE PRÁCTICA: Sistema de Renta de Bicicletas
-- Autor: Angel
-- Propósito: ejercicio de modelado, SQL y triggers en PostgreSQL,
--            en preparación para el proyecto real (Inventario Clínica)
-- ============================================================


-- ============================================================
-- 1. CREACIÓN DE TABLAS
-- Orden respeta las dependencias de llaves foráneas:
-- usuarios y bicicletas no dependen de nadie -> van primero
-- rentas depende de usuarios
-- cuenta depende de rentas y bicicletas
-- mantenimiento depende de bicicletas
-- ============================================================

CREATE TABLE usuarios (
    id_cliente SERIAL PRIMARY KEY,
    nombre     VARCHAR(100) NOT NULL,
    telefono   VARCHAR(10) NOT NULL UNIQUE,
    email      VARCHAR(100) UNIQUE NOT NULL
);

CREATE TABLE bicicletas (
    id_bici       SERIAL PRIMARY KEY,
    tipo          VARCHAR(20) CHECK (tipo IN ('Montaña', 'Ruta', 'Eléctrica')),
    contador_uso  INTEGER DEFAULT 0,
    estado        VARCHAR(20) CHECK (estado IN ('Disponible', 'En uso', 'En mantenimiento'))
                  DEFAULT 'Disponible'
);

CREATE TABLE rentas (
    id_renta         SERIAL PRIMARY KEY,
    id_cliente       INTEGER REFERENCES usuarios(id_cliente),
    duracion_pagada  INTERVAL NOT NULL,
    duracion_real    INTERVAL  -- queda en NULL hasta que se registre la devolución
);

-- Tabla intermedia: resuelve la relación muchos a muchos entre
-- rentas y bicicletas (una renta puede incluir varias bicis a la vez)
CREATE TABLE cuenta (
    id_renta INTEGER REFERENCES rentas(id_renta),
    id_bici  INTEGER REFERENCES bicicletas(id_bici),
    PRIMARY KEY (id_renta, id_bici)
);

CREATE TABLE mantenimiento (
    id_mantenimiento    SERIAL PRIMARY KEY,
    id_bici             INTEGER REFERENCES bicicletas(id_bici),
    fecha_mantenimiento DATE NOT NULL,
    notas_adicionales   TEXT
);


-- ============================================================
-- 2. DATOS DE PRUEBA
-- ============================================================

INSERT INTO usuarios (nombre, telefono, email)
VALUES
    ('Abril', '6561234567', 'abrilsa@gmail.com'),
    ('Angel', '6561016304', 'angel04@gmail.com'),
    ('Elizabeth', '6567809539', 'elizabeth10@gmail.com');

INSERT INTO bicicletas (tipo, contador_uso, estado)
VALUES
    ('Montaña', 0, 'Disponible'),
    ('Ruta', 10, 'En mantenimiento'),
    ('Eléctrica', 2, 'En uso');

-- Renta 1: cerrada (cliente ya regresó la bici antes de tiempo)
-- Renta 2: abierta (cliente Abril, id_cliente=1, aún tiene la bici)
INSERT INTO rentas (id_cliente, duracion_pagada, duracion_real)
VALUES
    (1, '2 hours', '1 hour'),
    (1, '1 day', NULL);

-- Renta 2 incluye DOS bicicletas a la vez (caso "familia")
INSERT INTO cuenta (id_renta, id_bici)
VALUES
    (2, 1),
    (2, 3);


-- ============================================================
-- 3. TRIGGERS — automatización de reglas de negocio
-- ============================================================

-- 3.1 Al insertar en `cuenta` (inicia una renta de una bici específica),
--     marcar esa bicicleta como 'En uso'
CREATE OR REPLACE FUNCTION marcar_bici_en_uso()
RETURNS TRIGGER AS $$
BEGIN
    UPDATE bicicletas
    SET estado = 'En uso'
    WHERE id_bici = NEW.id_bici;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trigger_bici_en_uso
AFTER INSERT ON cuenta
FOR EACH ROW
EXECUTE FUNCTION marcar_bici_en_uso();


-- 3.2 Al actualizar `rentas` y llenarse `duracion_real` (se registró
--     la devolución), liberar todas las bicis asociadas a esa renta
CREATE OR REPLACE FUNCTION liberar_bici()
RETURNS TRIGGER AS $$
BEGIN
    IF NEW.duracion_real IS NOT NULL THEN
        UPDATE bicicletas
        SET estado = 'Disponible', contador_uso = contador_uso + 1
        WHERE id_bici IN (
            SELECT id_bici FROM cuenta WHERE id_renta = NEW.id_renta
        );
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trigger_liberar_bici
AFTER UPDATE ON rentas
FOR EACH ROW
EXECUTE FUNCTION liberar_bici();


-- 3.3 Al insertar en `mantenimiento`, resetear el contador de uso
--     de la bicicleta correspondiente a 0
CREATE OR REPLACE FUNCTION resetear_contador()
RETURNS TRIGGER AS $$
BEGIN
    UPDATE bicicletas
    SET contador_uso = 0
    WHERE id_bici = NEW.id_bici;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trigger_resetear_contador
AFTER INSERT ON mantenimiento
FOR EACH ROW
EXECUTE FUNCTION resetear_contador();


-- ============================================================
-- 4. PRUEBAS DE LOS TRIGGERS
-- (datos y updates usados para verificar que cada trigger dispara
--  correctamente; se dejan documentados como evidencia del ejercicio)
-- ============================================================

-- Prueba trigger 3.1: nueva renta + nueva bici en cuenta -> debe
-- marcar la bici 2 (Ruta) como 'En uso' automáticamente
INSERT INTO rentas (id_cliente, duracion_pagada)
VALUES (3, '3 hours');

INSERT INTO cuenta (id_renta, id_bici)
VALUES (3, 2);

-- Prueba trigger 3.2: cerrar la renta 2 -> debe liberar bicis 1 y 3
UPDATE rentas
SET duracion_real = '2 hours'
WHERE id_renta = 2;

-- Prueba trigger 3.3: registrar mantenimiento a la bici 2 -> debe
-- resetear su contador_uso a 0
INSERT INTO mantenimiento (id_bici, fecha_mantenimiento, notas_adicionales)
VALUES (2, CURRENT_DATE, 'Mantenimiento de rutina');

-- Verificación visual del estado final de las bicicletas
SELECT * FROM bicicletas;


-- ============================================================
-- 5. CONSULTAS DE PRÁCTICA (JOIN)
-- ============================================================

-- 5.1 Tipo de bici + renta a la que pertenece
SELECT bicicletas.tipo, cuenta.id_renta
FROM bicicletas
JOIN cuenta ON bicicletas.id_bici = cuenta.id_bici;

-- 5.2 Cliente + tipo de bici que rentó + duración pagada
-- (encadena las 4 tablas: usuarios -> rentas -> cuenta -> bicicletas)
SELECT
    usuarios.id_cliente,
    usuarios.nombre,
    bicicletas.tipo,
    rentas.duracion_pagada
FROM rentas
JOIN usuarios  ON rentas.id_cliente = usuarios.id_cliente
JOIN cuenta    ON rentas.id_renta   = cuenta.id_renta
JOIN bicicletas ON cuenta.id_bici   = bicicletas.id_bici;
