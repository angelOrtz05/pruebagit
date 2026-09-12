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