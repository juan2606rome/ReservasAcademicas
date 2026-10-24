CREATE TABLE IF NOT EXISTS usuarios (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre TEXT NOT NULL,
    correo TEXT NOT NULL UNIQUE,
    hash_contraseña TEXT NOT NULL,
    rol TEXT NOT NULL CHECK(rol IN ('ADMINISTRADOR', 'SOLICITANTE')),
    activo INTEGER NOT NULL
);

CREATE TABLE IF NOT EXISTS espacios (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre TEXT NOT NULL,
    tipo TEXT NOT NULL CHECK(tipo IN ('LABORATORIO', 'AUDITORIO', 'SALA_COMPUTO')),
    capacidad INTEGER NOT NULL CHECK(capacidad > 0),
    activo INTEGER NOT NULL
);

CREATE UNIQUE INDEX IF NOT EXISTS idx_espacios_nombre_unique ON espacios (LOWER(TRIM(nombre)));

CREATE TABLE IF NOT EXISTS reservas (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    espacio_id INTEGER NOT NULL,
    usuario_id INTEGER NOT NULL,
    inicio TEXT NOT NULL,
    fin TEXT NOT NULL,
    motivo TEXT NOT NULL,
    estado TEXT NOT NULL CHECK(estado IN ('PENDIENTE', 'APROBADA', 'RECHAZADA', 'CANCELADA')),
    creada_en TEXT NOT NULL,
    FOREIGN KEY (espacio_id) REFERENCES espacios(id),
    FOREIGN KEY (usuario_id) REFERENCES usuarios(id),
    CHECK (fin > inicio)
);

CREATE INDEX IF NOT EXISTS idx_reservas_espacio ON reservas (espacio_id);
CREATE INDEX IF NOT EXISTS idx_reservas_usuario ON reservas (usuario_id);
CREATE INDEX IF NOT EXISTS idx_reservas_estado ON reservas (estado);
CREATE INDEX IF NOT EXISTS idx_reservas_espacio_tiempo ON reservas (espacio_id, inicio, fin);
