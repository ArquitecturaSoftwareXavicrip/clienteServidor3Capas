-- Esquema de base de datos - Tier 3: Acceso a Datos
-- Este archivo es de referencia. La base de datos se crea automáticamente con SQLAlchemy

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

-- Tabla de Empleados
CREATE TABLE IF NOT EXISTS empleados (
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    apellido VARCHAR(100) NOT NULL,
    email VARCHAR(100) NOT NULL UNIQUE,
    telefono VARCHAR(20),
    cargo VARCHAR(50),
    fecha_contratacion DATE DEFAULT CURRENT_DATE
);

-- Tabla de Espacios
CREATE TABLE IF NOT EXISTS espacios (
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    tipo VARCHAR(50) NOT NULL,
    empresa_id INTEGER NOT NULL,
    observaciones TEXT,
    FOREIGN KEY (empresa_id) REFERENCES empresas(id) ON DELETE CASCADE
);

-- Tabla de Asignaciones
CREATE TABLE IF NOT EXISTS asignaciones (
    id SERIAL PRIMARY KEY,
    contrato_id INTEGER NOT NULL,
    servicio_id INTEGER NOT NULL,
    empleado_id INTEGER NOT NULL,
    espacio_id INTEGER NOT NULL,
    fecha_inicio DATE NOT NULL,
    fecha_fin DATE,
    hora_inicio TIME NOT NULL,
    hora_fin TIME NOT NULL,
    frecuencia VARCHAR(20) NOT NULL,
    estado VARCHAR(20) NOT NULL DEFAULT 'ACTIVO',
    FOREIGN KEY (contrato_id) REFERENCES contratos(id),
    FOREIGN KEY (servicio_id) REFERENCES servicios(id),
    FOREIGN KEY (empleado_id) REFERENCES empleados(id),
    FOREIGN KEY (espacio_id) REFERENCES espacios(id)
);
