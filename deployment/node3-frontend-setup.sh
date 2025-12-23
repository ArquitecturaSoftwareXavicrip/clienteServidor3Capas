#!/bin/bash
# Node 3: Frontend Setup Script (Tier 1)
# Este script configura React App en el Nodo 3

set -e

echo "=== Configuración de Node 3: Frontend (Tier 1) ==="

# Paso 1: Preparar el entorno
echo "Paso 1: Preparando el entorno..."
sudo apt update && sudo apt upgrade -y

# Paso 2: Instalar Node.js y npm
echo "Paso 2: Instalando Node.js y npm..."
curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash -
sudo apt install -y nodejs

# Verificar instalación
echo "Versión de Node.js:"
node --version
echo "Versión de npm:"
npm --version

# Paso 3: Instalar Git
echo "Paso 3: Instalando Git..."
sudo apt install git -y

# Paso 4: Crear directorio para la aplicación
echo "Paso 4: Creando directorio de la aplicación..."
mkdir -p /opt/limpieza
cd /opt/limpieza

# Paso 5: Clonar repositorio
echo "Paso 5: Clonando repositorio..."
# Opción 1: Clonar desde GitHub
# git clone https://github.com/tu-usuario/arqCS-NCapas.git
# Opción 2: Copiar archivos manualmente
# scp -r usuario@tu-maquina:/ruta/al/proyecto ./arqCS-NCapas

cd arqCS-NCapas/frontend

# Paso 6: Instalar dependencias
echo "Paso 6: Instalando dependencias de npm..."
npm install

# Paso 7: Crear archivo .env
echo "Paso 7: Creando archivo .env..."
cat > .env <<EOF
PORT=3001
HOST=0.0.0.0
DANGEROUSLY_DISABLE_HOST_CHECK=true
REACT_APP_API_URL=http://192.168.1.20:5001/api
EOF

# Paso 8: Construir aplicación para producción
echo "Paso 8: Construyendo aplicación para producción..."
npm run build

# Verificar que se creó el directorio build/
ls -la build/

# Paso 9: Instalar Nginx
echo "Paso 9: Instalando Nginx..."
sudo apt install nginx -y

# Paso 10: Crear configuración de Nginx
echo "Paso 10: Configurando Nginx..."
sudo tee /etc/nginx/sites-available/limpieza-frontend > /dev/null <<'EOF'
server {
    listen 3001;
    server_name 192.168.1.30;

    root /opt/limpieza/arqCS-NCapas/frontend/build;
    index index.html;

    # Configuración para React Router
    location / {
        try_files $uri $uri/ /index.html;
    }

    # Configuración de archivos estáticos
    location /static {
        alias /opt/limpieza/arqCS-NCapas/frontend/build/static;
        expires 1y;
        add_header Cache-Control "public, immutable";
    }

    # Headers de seguridad
    add_header X-Frame-Options "SAMEORIGIN" always;
    add_header X-Content-Type-Options "nosniff" always;
    add_header X-XSS-Protection "1; mode=block" always;
}
EOF

# Paso 11: Habilitar sitio
echo "Paso 11: Habilitando sitio en Nginx..."
sudo ln -sf /etc/nginx/sites-available/limpieza-frontend /etc/nginx/sites-enabled/

# Paso 12: Verificar configuración de Nginx
echo "Paso 12: Verificando configuración de Nginx..."
sudo nginx -t

# Paso 13: Reiniciar Nginx
echo "Paso 13: Reiniciando Nginx..."
sudo systemctl restart nginx
sudo systemctl enable nginx

# Paso 14: Verificar estado de Nginx
echo "Paso 14: Verificando estado de Nginx..."
sudo systemctl status nginx

# Paso 15: Configurar Firewall
echo "Paso 15: Configurando Firewall..."
sudo ufw allow from 192.168.1.0/24 to any port 3001
sudo ufw allow 'Nginx Full'
sudo ufw enable
sudo ufw status

# Paso 16: Verificar que el frontend funciona
echo "Paso 16: Verificando que el frontend funciona..."
sleep 2
curl http://192.168.1.30:3001/ | head -20

echo "=== Node 3 (Frontend) configurado exitosamente ==="
echo "Frontend está escuchando en 192.168.1.30:3001"
echo "Ver logs: sudo tail -f /var/log/nginx/access.log"
