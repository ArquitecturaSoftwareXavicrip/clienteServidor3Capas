#!/bin/bash
# Script para configurar NODO 1: Base de Datos (PostgreSQL)
# Para video de demostración

echo "======================================"
echo "NODO 1: Configuración de PostgreSQL"
echo "======================================"
echo ""

# Colores
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

# Obtener IP
IP=$(hostname -I | awk '{print $1}')
echo -e "${BLUE}IP de este nodo: $IP${NC}"
echo ""

# Instalar PostgreSQL
echo "Instalando PostgreSQL..."
sudo apt update
sudo apt install postgresql postgresql-contrib -y

# Iniciar servicio
sudo systemctl start postgresql
sudo systemctl enable postgresql

# Crear base de datos
echo "Creando base de datos..."
sudo -u postgres psql -c "CREATE DATABASE limpieza_empresas;" 2>/dev/null

# Crear tablas (asume que schema.sql está en ../database/)
echo "Creando tablas..."
cd ../database
sudo -u postgres psql limpieza_empresas -f schema.sql

# Configurar acceso remoto
echo "Configurando acceso remoto..."
sudo sed -i "s/#listen_addresses = 'localhost'/listen_addresses = '*'/" /etc/postgresql/*/main/postgresql.conf
echo "host    limpieza_empresas    postgres    192.168.1.0/24    trust" | sudo tee -a /etc/postgresql/*/main/pg_hba.conf

# Reiniciar PostgreSQL
sudo systemctl restart postgresql

# Configurar firewall
echo "Configurando firewall..."
sudo ufw allow from 192.168.1.0/24 to any port 5432
sudo ufw --force enable

echo ""
echo -e "${GREEN}======================================"
echo "✅ NODO 1 Configurado Exitosamente"
echo "======================================${NC}"
echo ""
echo -e "${YELLOW}Información del Nodo:${NC}"
echo "  IP: $IP"
echo "  Puerto: 5432"
echo "  Base de Datos: limpieza_empresas"
echo ""
echo -e "${YELLOW}Comandos útiles:${NC}"
echo "  # Conectar a BD:"
echo "  sudo -u postgres psql limpieza_empresas"
echo ""
echo "  # Ver permisos en tiempo real:"
echo "  watch -n 2 'psql -U postgres -d limpieza_empresas -c \"SELECT * FROM permisos ORDER BY id DESC LIMIT 5;\"'"
echo ""
echo -e "${GREEN}Siguiente paso: Configurar Nodo 2 (Backend)${NC}"
echo ""

