#!/bin/bash
# Script para configurar NODO 2: Backend (Flask API)
# Para video de demostración

echo "======================================"
echo "NODO 2: Configuración de Backend"
echo "======================================"
echo ""

# Colores
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
RED='\033[0;31m'
NC='\033[0m'

# Obtener IP
IP=$(hostname -I | awk '{print $1}')
echo -e "${BLUE}IP de este nodo: $IP${NC}"
echo ""

# Solicitar IP del Nodo 1
read -p "IP del Nodo 1 (PostgreSQL) [192.168.1.10]: " DB_IP
DB_IP=${DB_IP:-192.168.1.10}

read -p "IP del Nodo 3 (Frontend) [192.168.1.30]: " FRONTEND_IP
FRONTEND_IP=${FRONTEND_IP:-192.168.1.30}

# Instalar dependencias
echo "Instalando dependencias..."
sudo apt update
sudo apt install python3 python3-pip python3-venv git postgresql-client -y

# Crear directorio y clonar
echo "Clonando repositorio..."
mkdir -p /opt/limpieza
cd /opt/limpieza
git clone https://github.com/samuelanyoneai/clienteServidor3Capas.git
cd clienteServidor3Capas/backend

# Crear entorno virtual
echo "Configurando entorno virtual..."
python3 -m venv venv
source venv/bin/activate

# Instalar dependencias Python
pip install --upgrade pip
pip install -r requirements.txt
pip install psycopg2-binary

# Crear archivo .env
echo "Creando archivo .env..."
cat > .env << EOF
FLASK_ENV=production
PORT=5001
SECRET_KEY=$(openssl rand -hex 32)
SQLALCHEMY_DATABASE_URI=postgresql://postgres@${DB_IP}:5432/limpieza_empresas
CORS_ORIGINS=http://${FRONTEND_IP}:3001,http://localhost:3001
EOF

# Verificar conexión a PostgreSQL
echo "Verificando conexión a PostgreSQL..."
if psql -h $DB_IP -U postgres -d limpieza_empresas -c "SELECT 1;" &> /dev/null; then
    echo -e "${GREEN}✓ Conexión a PostgreSQL exitosa${NC}"
else
    echo -e "${RED}✗ No se puede conectar a PostgreSQL${NC}"
    echo "Verifica que el Nodo 1 esté configurado correctamente"
    exit 1
fi

# Cargar datos de ejemplo
echo "Cargando datos de ejemplo..."
cd ../database
python3 init_db.py
python3 init_permisos.py
python3 init_empleados.py
cd ../backend

# Crear servicio systemd
echo "Creando servicio systemd..."
sudo tee /etc/systemd/system/limpieza-backend.service > /dev/null << EOF
[Unit]
Description=Limpieza Backend Service
After=network.target

[Service]
Type=simple
User=$USER
WorkingDirectory=/opt/limpieza/clienteServidor3Capas/backend
Environment="PATH=/opt/limpieza/clienteServidor3Capas/backend/venv/bin"
EnvironmentFile=/opt/limpieza/clienteServidor3Capas/backend/.env
ExecStart=/opt/limpieza/clienteServidor3Capas/backend/venv/bin/python run.py
Restart=always

[Install]
WantedBy=multi-user.target
EOF

sudo systemctl daemon-reload
sudo systemctl enable limpieza-backend
sudo systemctl start limpieza-backend

# Configurar firewall
echo "Configurando firewall..."
sudo ufw allow from 192.168.1.0/24 to any port 5001
sudo ufw --force enable

echo ""
echo -e "${GREEN}======================================"
echo "✅ NODO 2 Configurado Exitosamente"
echo "======================================${NC}"
echo ""
echo -e "${YELLOW}Información del Nodo:${NC}"
echo "  IP: $IP"
echo "  Puerto: 5001"
echo "  API Base: http://$IP:5001"
echo ""
echo -e "${YELLOW}Verificar funcionamiento:${NC}"
echo "  curl http://localhost:5001/"
echo "  curl http://localhost:5001/api/permisos"
echo ""
echo -e "${YELLOW}Ver logs:${NC}"
echo "  sudo journalctl -u limpieza-backend -f"
echo ""
echo -e "${GREEN}Siguiente paso: Configurar Nodo 3 (Frontend)${NC}"
echo ""

