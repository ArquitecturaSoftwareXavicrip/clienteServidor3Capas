#!/bin/bash
# Node 2: Backend Setup Script (Tier 2)
# Este script configura Flask API en el Nodo 2

set -e

echo "=== Configuración de Node 2: Backend (Tier 2) ==="

# Paso 1: Preparar el entorno
echo "Paso 1: Preparando el entorno..."
sudo apt update && sudo apt upgrade -y
sudo apt install python3 python3-pip python3-venv git postgresql-client -y

# Paso 2: Crear directorio para la aplicación
echo "Paso 2: Creando directorio de la aplicación..."
mkdir -p /opt/limpieza
cd /opt/limpieza

# Paso 3: Clonar repositorio (o copiar archivos)
echo "Paso 3: Clonando repositorio..."
# Opción 1: Clonar desde GitHub
# git clone https://github.com/tu-usuario/arqCS-NCapas.git
# Opción 2: Copiar archivos manualmente (si no tienes acceso a GitHub)
# scp -r usuario@tu-maquina:/ruta/al/proyecto ./arqCS-NCapas

cd arqCS-NCapas/backend

# Paso 4: Crear entorno virtual
echo "Paso 4: Creando entorno virtual..."
python3 -m venv venv
source venv/bin/activate

# Paso 5: Instalar dependencias
echo "Paso 5: Instalando dependencias..."
pip install --upgrade pip
pip install -r requirements.txt

# Paso 6: Crear archivo .env
echo "Paso 6: Creando archivo .env..."
cat > .env <<EOF
FLASK_ENV=production
SQLALCHEMY_DATABASE_URI=postgresql://limpieza_user:contraseña_segura_123@192.168.1.10:5432/limpieza_empresas
PORT=5001
SECRET_KEY=tu-clave-secreta-super-segura-aqui-cambiar-en-produccion
CORS_ORIGINS=http://192.168.1.30:3001,http://localhost:3001
EOF

# Paso 7: Probar conexión a base de datos
echo "Paso 7: Probando conexión a base de datos..."
psql -h 192.168.1.10 -U limpieza_user -d limpieza_empresas -c "SELECT version();"

# Paso 8: Inicializar base de datos
echo "Paso 8: Inicializando base de datos..."
source venv/bin/activate
cd ../database
python3 init_db.py
cd ../backend

# Paso 9: Crear servicio systemd
echo "Paso 9: Creando servicio systemd..."
sudo tee /etc/systemd/system/limpieza-backend.service > /dev/null <<EOF
[Unit]
Description=Limpieza Backend Service (Tier 2)
After=network.target postgresql.service

[Service]
Type=simple
User=www-data
WorkingDirectory=/opt/limpieza/arqCS-NCapas/backend
Environment="PATH=/opt/limpieza/arqCS-NCapas/backend/venv/bin"
EnvironmentFile=/opt/limpieza/arqCS-NCapas/backend/.env
ExecStart=/opt/limpieza/arqCS-NCapas/backend/venv/bin/python run.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
EOF

# Paso 10: Recargar systemd y habilitar servicio
echo "Paso 10: Habilitando servicio..."
sudo systemctl daemon-reload
sudo systemctl enable limpieza-backend
sudo systemctl start limpieza-backend

# Paso 11: Verificar estado
echo "Paso 11: Verificando estado del servicio..."
sudo systemctl status limpieza-backend

# Paso 12: Configurar Firewall
echo "Paso 12: Configurando Firewall..."
sudo ufw allow from 192.168.1.0/24 to any port 5001
sudo ufw enable
sudo ufw status

# Paso 13: Verificar que el backend funciona
echo "Paso 13: Verificando que el backend funciona..."
sleep 2
curl http://192.168.1.20:5001/

echo "=== Node 2 (Backend) configurado exitosamente ==="
echo "Backend está escuchando en 192.168.1.20:5001"
echo "Ver logs: sudo journalctl -u limpieza-backend -f"
