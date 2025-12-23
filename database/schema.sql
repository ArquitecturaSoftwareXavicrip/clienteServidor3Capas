-- Esquema de base de datos - Tier 3: Acceso a Datos
-- PostgreSQL Schema para despliegue en 3 nodos

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

-- Tabla de Permisos (Vacaciones)
CREATE TABLE IF NOT EXISTS permisos (
    id SERIAL PRIMARY KEY,
    empleado VARCHAR(100) NOT NULL,
    tipo VARCHAR(50) NOT NULL DEFAULT 'Vacaciones',
    fecha_inicio DATE NOT NULL,
    fecha_fin DATE NOT NULL,
    dias_solicitados INTEGER NOT NULL,
    estado VARCHAR(20) NOT NULL DEFAULT 'pendiente',
    observaciones TEXT
);

-- Tabla de Empleados
CREATE TABLE IF NOT EXISTS empleados (
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    apellido VARCHAR(100) NOT NULL,
    email VARCHAR(100) NOT NULL,
    telefono VARCHAR(20) NOT NULL,
    cargo VARCHAR(50) NOT NULL
);

-- Índices para mejorar rendimiento
CREATE INDEX IF NOT EXISTS idx_contratos_empresa ON contratos(empresa_id);
CREATE INDEX IF NOT EXISTS idx_contratos_servicio ON contratos(servicio_id);
CREATE INDEX IF NOT EXISTS idx_permisos_estado ON permisos(estado);
CREATE INDEX IF NOT EXISTS idx_permisos_empleado ON permisos(empleado);
CREATE INDEX IF NOT EXISTS idx_empleados_email ON empleados(email);
CREATE INDEX IF NOT EXISTS idx_empleados_cargo ON empleados(cargo);



