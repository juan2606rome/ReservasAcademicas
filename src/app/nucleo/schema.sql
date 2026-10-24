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
    decidido_por INTEGER,
    decidido_en TEXT,
    motivo_decision TEXT,
    FOREIGN KEY (espacio_id) REFERENCES espacios(id),
    FOREIGN KEY (usuario_id) REFERENCES usuarios(id),
    FOREIGN KEY (decidido_por) REFERENCES usuarios(id),
    CHECK (fin > inicio)
);

CREATE INDEX IF NOT EXISTS idx_reservas_espacio ON reservas (espacio_id);
CREATE INDEX IF NOT EXISTS idx_reservas_usuario ON reservas (usuario_id);
CREATE INDEX IF NOT EXISTS idx_reservas_estado ON reservas (estado);
CREATE INDEX IF NOT EXISTS idx_reservas_espacio_tiempo ON reservas (espacio_id, inicio, fin);

CREATE TABLE IF NOT EXISTS HistorialReserva (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    reserva_id INTEGER NOT NULL,
    estado_anterior TEXT,
    estado_nuevo TEXT NOT NULL,
    cambiado_por INTEGER NOT NULL,
    cambiado_en TEXT NOT NULL,
    comentario TEXT,
    FOREIGN KEY (reserva_id) REFERENCES reservas(id),
    FOREIGN KEY (cambiado_por) REFERENCES usuarios(id)
);

CREATE INDEX IF NOT EXISTS idx_historial_reserva ON HistorialReserva (reserva_id);
CREATE INDEX IF NOT EXISTS idx_historial_cambiado_en ON HistorialReserva (cambiado_en);
CREATE INDEX IF NOT EXISTS idx_historial_estado_nuevo ON HistorialReserva (estado_nuevo);
