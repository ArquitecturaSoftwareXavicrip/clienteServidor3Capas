#!/bin/bash
# Script para configurar Frontend React
# Tier 1: Presentación

echo "=================================="
echo "Setup Frontend React - Nodo 3"
echo "=================================="
echo ""

# Colores
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Verificar Node.js
if ! command -v node &> /dev/null; then
    echo -e "${RED}Node.js no está instalado${NC}"
    echo "Instalando Node.js 18..."
    curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash -
    sudo apt install -y nodejs
fi

echo -e "${GREEN}✓ Node.js está instalado${NC}"
node --version
npm --version
echo ""

# Instalar dependencias
if [ ! -d "node_modules" ]; then
    echo "Instalando dependencias npm..."
    npm install
    echo -e "${GREEN}✓ Dependencias instaladas${NC}"
else
    echo -e "${YELLOW}⚠ node_modules ya existe${NC}"
    read -p "¿Reinstalar dependencias? (s/n): " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Ss]$ ]]; then
        rm -rf node_modules package-lock.json
        npm install
        echo -e "${GREEN}✓ Dependencias reinstaladas${NC}"
    fi
fi
echo ""

# Crear archivo .env si no existe
if [ ! -f ".env" ]; then
    echo "Creando archivo .env..."
    
    read -p "IP del Nodo 2 (Backend) [192.168.1.20]: " BACKEND_HOST
    BACKEND_HOST=${BACKEND_HOST:-192.168.1.20}
    
    cat > .env << EOF
REACT_APP_API_URL=http://${BACKEND_HOST}:5001/api
PORT=3001
EOF
    
    echo -e "${GREEN}✓ Archivo .env creado${NC}"
else
    echo -e "${YELLOW}⚠ El archivo .env ya existe${NC}"
    cat .env
fi
echo ""

# Preguntar si desea construir para producción
read -p "¿Construir para producción con Nginx? (s/n): " -n 1 -r
echo
if [[ $REPLY =~ ^[Ss]$ ]]; then
    echo "Construyendo aplicación..."
    npm run build
    
    if [ $? -eq 0 ]; then
        echo -e "${GREEN}✓ Build completado${NC}"
        echo ""
        
        # Configurar Nginx
        read -p "¿Configurar Nginx? (s/n): " -n 1 -r
        echo
        if [[ $REPLY =~ ^[Ss]$ ]]; then
            # Instalar Nginx si no está instalado
            if ! command -v nginx &> /dev/null; then
                echo "Instalando Nginx..."
                sudo apt install nginx -y
            fi
            
            WORK_DIR=$(pwd)
            
            sudo tee /etc/nginx/sites-available/limpieza-frontend > /dev/null << EOF
server {
    listen 3001;
    server_name _;

    root $WORK_DIR/build;
    index index.html;

    # React Router
    location / {
        try_files \$uri \$uri/ /index.html;
    }

    # Archivos estáticos
    location /static {
        alias $WORK_DIR/build/static;
        expires 1y;
        add_header Cache-Control "public, immutable";
    }

    # Headers de seguridad
    add_header X-Frame-Options "SAMEORIGIN" always;
    add_header X-Content-Type-Options "nosniff" always;
    add_header X-XSS-Protection "1; mode=block" always;
}
EOF
            
            # Habilitar sitio
            sudo ln -sf /etc/nginx/sites-available/limpieza-frontend /etc/nginx/sites-enabled/
            
            # Verificar configuración
            sudo nginx -t
            
            if [ $? -eq 0 ]; then
                sudo systemctl restart nginx
                sudo systemctl enable nginx
                echo -e "${GREEN}✓ Nginx configurado${NC}"
            else
                echo -e "${RED}✗ Error en configuración de Nginx${NC}"
            fi
        fi
    else
        echo -e "${RED}✗ Error al construir aplicación${NC}"
    fi
else
    echo "Puedes ejecutar 'npm start' para modo desarrollo"
fi
echo ""

# Verificar conexión al backend
echo "Verificando conexión al backend..."
BACKEND_URL=$(grep REACT_APP_API_URL .env | cut -d'=' -f2 | sed 's|/api||')

if curl -s "$BACKEND_URL/" > /dev/null; then
    echo -e "${GREEN}✓ Conexión al backend exitosa${NC}"
else
    echo -e "${RED}✗ No se puede conectar al backend${NC}"
    echo "Verifica que:"
    echo "1. El backend está corriendo en Nodo 2"
    echo "2. El firewall permite el puerto 5001"
    echo "3. CORS está configurado correctamente"
fi
echo ""

echo -e "${GREEN}=================================="
echo "✓ Setup completado exitosamente"
echo "==================================${NC}"
echo ""
echo "Próximos pasos:"
echo "Modo Desarrollo:"
echo "  npm start"
echo ""
echo "Modo Producción (si configuraste Nginx):"
echo "  Acceder a: http://$(hostname -I | awk '{print $1}'):3001"
echo ""
echo "Verificar estado de Nginx:"
echo "  sudo systemctl status nginx"
echo ""

