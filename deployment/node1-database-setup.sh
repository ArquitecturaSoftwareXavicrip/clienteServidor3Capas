#!/bin/bash
# Node 1: Database Setup Script (Tier 3)
# Este script configura PostgreSQL en el Nodo 1

set -e

echo "=== Configuración de Node 1: Base de Datos (Tier 3) ==="

# Paso 1: Actualizar sistema
echo "Paso 1: Actualizando sistema..."
sudo apt update && sudo apt upgrade -y

# Paso 2: Instalar PostgreSQL
echo "Paso 2: Instalando PostgreSQL..."
sudo apt install postgresql postgresql-contrib -y

# Paso 3: Verificar instalación
echo "Paso 3: Verificando instalación de PostgreSQL..."
sudo systemctl status postgresql

# Paso 4: Crear base de datos y usuario
echo "Paso 4: Creando base de datos y usuario..."
sudo -u postgres psql <<EOF
CREATE DATABASE limpieza_empresas;
CREATE USER limpieza_user WITH PASSWORD 'contraseña_segura_123';
GRANT ALL PRIVILEGES ON DATABASE limpieza_empresas TO limpieza_user;
ALTER USER limpieza_user CREATEDB;
\q
EOF

# Paso 5: Configurar acceso remoto
echo "Paso 5: Configurando acceso remoto..."
# Editar postgresql.conf para escuchar en todas las interfaces
sudo sed -i "s/#listen_addresses = 'localhost'/listen_addresses = '*'/g" /etc/postgresql/*/main/postgresql.conf

# Agregar configuración a pg_hba.conf
echo "host    limpieza_empresas    limpieza_user    192.168.1.0/24    md5" | sudo tee -a /etc/postgresql/*/main/pg_hba.conf

# Paso 6: Reiniciar PostgreSQL
echo "Paso 6: Reiniciando PostgreSQL..."
sudo systemctl restart postgresql
sudo systemctl enable postgresql

# Paso 7: Verificar que está escuchando
echo "Paso 7: Verificando que PostgreSQL escucha en todas las interfaces..."
sudo netstat -tulpn | grep 5432

# Paso 8: Configurar Firewall
echo "Paso 8: Configurando Firewall..."
sudo ufw allow from 192.168.1.0/24 to any port 5432
sudo ufw enable
sudo ufw status

# Paso 9: Crear esquema de base de datos
echo "Paso 9: Creando esquema de base de datos..."
sudo -u postgres psql limpieza_empresas <<EOF
CREATE TABLE IF NOT EXISTS empresas (
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    direccion VARCHAR(200) NOT NULL,
    telefono VARCHAR(20) NOT NULL,
    email VARCHAR(100) NOT NULL
);

CREATE TABLE IF NOT EXISTS servicios (
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    descripcion TEXT,
    precio_base REAL NOT NULL,
    duracion_horas REAL NOT NULL
);

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
EOF

echo "=== Node 1 (Database) configurado exitosamente ==="
echo "PostgreSQL está escuchando en 192.168.1.10:5432"
echo "Base de datos: limpieza_empresas"
echo "Usuario: limpieza_user"
