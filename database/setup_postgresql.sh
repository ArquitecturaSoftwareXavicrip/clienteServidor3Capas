#!/bin/bash
# Script para configurar PostgreSQL para el proyecto
# Tier 3: Base de Datos

echo "=================================="
echo "Setup PostgreSQL - Nodo 1"
echo "=================================="
echo ""

# Colores
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Verificar si PostgreSQL está instalado
if ! command -v psql &> /dev/null; then
    echo -e "${RED}PostgreSQL no está instalado.${NC}"
    echo "Instalando PostgreSQL..."
    sudo apt update
    sudo apt install postgresql postgresql-contrib -y
fi

echo -e "${GREEN}✓ PostgreSQL está instalado${NC}"
echo ""

# Verificar si el servicio está corriendo
if ! systemctl is-active --quiet postgresql; then
    echo "Iniciando PostgreSQL..."
    sudo systemctl start postgresql
    sudo systemctl enable postgresql
fi

echo -e "${GREEN}✓ PostgreSQL está corriendo${NC}"
echo ""

# Crear base de datos
echo "Creando base de datos..."
sudo -u postgres psql -c "CREATE DATABASE limpieza_empresas;" 2>/dev/null
if [ $? -eq 0 ]; then
    echo -e "${GREEN}✓ Base de datos 'limpieza_empresas' creada${NC}"
else
    echo -e "${YELLOW}⚠ La base de datos ya existe${NC}"
fi
echo ""

# Crear tablas
echo "Creando tablas..."
sudo -u postgres psql limpieza_empresas -f schema.sql
if [ $? -eq 0 ]; then
    echo -e "${GREEN}✓ Tablas creadas${NC}"
else
    echo -e "${RED}✗ Error al crear tablas${NC}"
    exit 1
fi
echo ""

# Configurar acceso remoto (si se desea)
read -p "¿Configurar acceso remoto? (s/n): " -n 1 -r
echo
if [[ $REPLY =~ ^[Ss]$ ]]; then
    echo "Configurando acceso remoto..."
    
    # Backup de archivos de configuración
    sudo cp /etc/postgresql/*/main/postgresql.conf /etc/postgresql/*/main/postgresql.conf.bak
    sudo cp /etc/postgresql/*/main/pg_hba.conf /etc/postgresql/*/main/pg_hba.conf.bak
    
    # Configurar listen_addresses
    sudo sed -i "s/#listen_addresses = 'localhost'/listen_addresses = '*'/" /etc/postgresql/*/main/postgresql.conf
    
    # Agregar regla de acceso trust para red local
    echo "host    limpieza_empresas    postgres    192.168.1.0/24    trust" | sudo tee -a /etc/postgresql/*/main/pg_hba.conf
    
    # Reiniciar PostgreSQL
    sudo systemctl restart postgresql
    
    echo -e "${GREEN}✓ Acceso remoto configurado${NC}"
    echo -e "${YELLOW}⚠ Recuerda configurar el firewall:${NC}"
    echo "  sudo ufw allow from 192.168.1.0/24 to any port 5432"
    echo ""
fi

# Verificar tablas
echo "Verificando tablas..."
TABLES=$(sudo -u postgres psql limpieza_empresas -t -c "SELECT tablename FROM pg_tables WHERE schemaname='public';")
echo -e "${GREEN}Tablas creadas:${NC}"
echo "$TABLES"
echo ""

echo -e "${GREEN}=================================="
echo "✓ Setup completado exitosamente"
echo "==================================${NC}"
echo ""
echo "Próximos pasos:"
echo "1. Cargar datos de ejemplo: python3 init_db.py"
echo "2. Cargar permisos de ejemplo: python3 init_permisos.py"
echo "3. Configurar Nodo 2 (Backend)"
echo ""

