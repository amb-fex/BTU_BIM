CREATE DATABASE btu_bim;

CREATE TYPE geometria_tipo AS ENUM ('punto', 'línea', 'polígono');

CREATE TABLE datos_btu_bim (
    id SERIAL PRIMARY KEY,
    categoria VARCHAR(20) NOT NULL,
    elemento_objeto VARCHAR(50) NOT NULL,
    descripcion TEXT,
    tipo VARCHAR(5) NOT NULL,
    geometria geometria_tipo NOT NULL, -- Usamos el tipo ENUM
    terreno TEXT[], -- Lo definiremos ñuego para el desplegable lista
    captacion TEXT,
    fotografias BYTEA,
    observaciones TEXT
);
CREATE TABLE terreno_valores (
    id SERIAL PRIMARY KEY,
    valor VARCHAR(50) UNIQUE NOT NULL -- Los valores fijos de terreno
);

INSERT INTO terreno_valores (valor)
VALUES
('terreno'),
('sobresale'),
('sobre construcción'),
('elevado'),
('en túnel'),
('bajo tierra'),
('otro');

CREATE TABLE datos_btu_bim_terreno (
    id SERIAL PRIMARY KEY,
    datos_btu_bim_id INT REFERENCES datos_btu_bim(id) ON DELETE CASCADE, -- Relación con la tabla principal
    terreno_id INT REFERENCES terreno_valores(id) ON DELETE CASCADE -- Relación con los valores de terreno
);

