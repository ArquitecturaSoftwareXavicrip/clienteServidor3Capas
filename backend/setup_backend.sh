#!/bin/bash
# Script para configurar Backend Flask
# Tier 2: Lógica de Negocio

echo "=================================="
echo "Setup Backend Flask - Nodo 2"
echo "=================================="
echo ""

# Colores
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Verificar Python
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}Python3 no está instalado${NC}"
    echo "Instalando Python3..."
    sudo apt update
    sudo apt install python3 python3-pip python3-venv -y
fi

echo -e "${GREEN}✓ Python3 está instalado${NC}"
python3 --version
echo ""

# Crear entorno virtual
if [ ! -d "venv" ]; then
    echo "Creando entorno virtual..."
    python3 -m venv venv
    echo -e "${GREEN}✓ Entorno virtual creado${NC}"
else
    echo -e "${YELLOW}⚠ El entorno virtual ya existe${NC}"
fi
echo ""

# Activar entorno virtual
echo "Activando entorno virtual..."
source venv/bin/activate

# Instalar dependencias
echo "Instalando dependencias..."
pip install --upgrade pip
pip install -r requirements.txt
pip install psycopg2-binary
echo -e "${GREEN}✓ Dependencias instaladas${NC}"
echo ""

# Crear archivo .env si no existe
if [ ! -f ".env" ]; then
    echo "Creando archivo .env..."
    
    read -p "IP del Nodo 1 (PostgreSQL) [192.168.1.10]: " DB_HOST
    DB_HOST=${DB_HOST:-192.168.1.10}
    
    read -p "IP del Nodo 3 (Frontend) [192.168.1.30]: " FRONTEND_HOST
    FRONTEND_HOST=${FRONTEND_HOST:-192.168.1.30}
    
    cat > .env << EOF
FLASK_ENV=production
PORT=5001
SECRET_KEY=$(openssl rand -hex 32)

# PostgreSQL SIN contraseña
SQLALCHEMY_DATABASE_URI=postgresql://postgres@${DB_HOST}:5432/limpieza_empresas

# CORS
CORS_ORIGINS=http://${FRONTEND_HOST}:3001,http://localhost:3001
EOF
    
    echo -e "${GREEN}✓ Archivo .env creado${NC}"
else
    echo -e "${YELLOW}⚠ El archivo .env ya existe${NC}"
fi
echo ""

# Verificar conexión a PostgreSQL
echo "Verificando conexión a PostgreSQL..."
read -p "IP del Nodo 1 (PostgreSQL) [192.168.1.10]: " DB_HOST
DB_HOST=${DB_HOST:-192.168.1.10}

if psql -h $DB_HOST -U postgres -d limpieza_empresas -c "SELECT 1;" &> /dev/null; then
    echo -e "${GREEN}✓ Conexión a PostgreSQL exitosa${NC}"
else
    echo -e "${RED}✗ No se puede conectar a PostgreSQL${NC}"
    echo "Verifica que:"
    echo "1. PostgreSQL está corriendo en Nodo 1"
    echo "2. pg_hba.conf permite conexiones desde este nodo"
    echo "3. El firewall permite el puerto 5432"
fi
echo ""

# Preguntar si desea inicializar datos
read -p "¿Inicializar base de datos con datos de ejemplo? (s/n): " -n 1 -r
echo
if [[ $REPLY =~ ^[Ss]$ ]]; then
    echo "Inicializando base de datos..."
    cd ../database
    python3 init_db.py
    python3 init_permisos.py
    cd ../backend
    echo -e "${GREEN}✓ Datos de ejemplo cargados${NC}"
fi
echo ""

# Preguntar si desea crear servicio systemd
read -p "¿Crear servicio systemd? (s/n): " -n 1 -r
echo
if [[ $REPLY =~ ^[Ss]$ ]]; then
    WORK_DIR=$(pwd)
    
    sudo tee /etc/systemd/system/limpieza-backend.service > /dev/null << EOF
[Unit]
Description=Limpieza Backend Service (Tier 2)
After=network.target

[Service]
Type=simple
User=$USER
WorkingDirectory=$WORK_DIR
Environment="PATH=$WORK_DIR/venv/bin"
EnvironmentFile=$WORK_DIR/.env
ExecStart=$WORK_DIR/venv/bin/python run.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
EOF
    
    sudo systemctl daemon-reload
    sudo systemctl enable limpieza-backend
    sudo systemctl start limpieza-backend
    
    echo -e "${GREEN}✓ Servicio systemd creado y habilitado${NC}"
    echo ""
    echo "Ver estado: sudo systemctl status limpieza-backend"
    echo "Ver logs: sudo journalctl -u limpieza-backend -f"
fi
echo ""

echo -e "${GREEN}=================================="
echo "✓ Setup completado exitosamente"
echo "==================================${NC}"
echo ""
echo "Próximos pasos:"
echo "1. Iniciar backend: python run.py"
echo "2. O si creaste el servicio: sudo systemctl status limpieza-backend"
echo "3. Probar API: curl http://localhost:5001/"
echo "4. Configurar Nodo 3 (Frontend)"
echo ""

