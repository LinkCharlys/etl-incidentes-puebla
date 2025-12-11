-- setup_db.sql
DROP TABLE IF EXISTS road_incidents;

CREATE TABLE road_incidents (
    id_incidente VARCHAR(255) PRIMARY KEY,
    fecha DATE,
    hora TIME,
    dia_semana VARCHAR(50),
    tipo_incidente VARCHAR(255),
    delegacion VARCHAR(255),
    colonia VARCHAR(255),
    tipo_hecho VARCHAR(255),
    lesionados INTEGER,
    muertos INTEGER,
    vehiculos_involucrados INTEGER,
    longitud NUMERIC(10, 7),
    latitud NUMERIC(10, 7)
);