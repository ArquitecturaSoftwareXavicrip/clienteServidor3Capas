-- Esquema de base de datos - Tier 3: Acceso a Datos
-- Compatible con PostgreSQL

-- Tabla de Empresas
CREATE TABLE IF NOT EXISTS empresas (
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    direccion VARCHAR(200) NOT NULL,
    telefono VARCHAR(20) NOT NULL,
    email VARCHAR(100) NOT NULL
);

-- Tabla de Servicios
CREATE TABLE IF NOT EXISTS servicios (
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    descripcion TEXT,
    precio_base REAL NOT NULL,
    duracion_horas REAL NOT NULL
);

-- Tabla de Contratos
CREATE TABLE IF NOT EXISTS contratos (
    id SERIAL PRIMARY KEY,
    empresa_id INTEGER NOT NULL,
    servicio_id INTEGER NOT NULL,
    fecha_inicio DATE NOT NULL,
    fecha_fin DATE,
    estado VARCHAR(20) NOT NULL DEFAULT 'activo',
    precio_final REAL NOT NULL,
    FOREIGN KEY (empresa_id) REFERENCES empresas(id) ON DELETE CASCADE,
    FOREIGN KEY (servicio_id) REFERENCES servicios(id) ON DELETE CASCADE
);



