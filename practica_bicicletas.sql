CREATE TABLE usuarios (
	id_cliente SERIAL PRIMARY KEY,
	nombre VARCHAR(100) NOT NULL,
	telefono VARCHAR(10) NOT NULL UNIQUE,
	email VARCHAR(100) UNIQUE NOT NULL
);
CREATE TABLE bicicletas (
	id_bici SERIAL PRIMARY KEY,
	tipo VARCHAR(20) CHECK (tipo IN ('Montaña', 'Ruta', 'Eléctrica')),
	contador_uso INTEGER DEFAULT 0,
	estado VARCHAR(20) CHECK (estado IN ('Disponible', 'En uso', 'En mantenimiento')) DEFAULT 'Disponible' 
);
CREATE TABLE rentas (
	id_renta SERIAL PRIMARY KEY,
	id_cliente INTEGER REFERENCES usuarios(id_cliente),
	duracion_pagada INTERVAL NOT NULL,
	duracion_real INTERVAL 
);
CREATE TABLE cuenta (
	id_renta INTEGER REFERENCES rentas(id_renta),
	id_bici INTEGER REFERENCES bicicletas(id_bici),
	PRIMARY KEY (id_renta, id_bici)
);
CREATE TABLE mantenimiento (
	id_mantenimiento SERIAL PRIMARY KEY,
	id_bici INTEGER REFERENCES bicicletas(id_bici),
	fecha_mantenimiento DATE NOT NULL,
	notas_adicionales TEXT
);
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

INSERT INTO rentas(id_cliente,duracion_pagada,duracion_real)
VALUES
	(1,'2 hours','1 hour'),
	(1,'1 day',null);

INSERT INTO cuenta(id_renta,id_bici)
VALUES
	(2,1),
	(2,3);


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



INSERT INTO rentas (id_cliente, duracion_pagada)
VALUES (3, '3 hours');

INSERT INTO cuenta (id_renta, id_bici)
VALUES (3, 2);

SELECT * FROM bicicletas;