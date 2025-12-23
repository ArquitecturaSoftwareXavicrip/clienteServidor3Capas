#!/bin/bash
# Script para probar conectividad entre nodos
# Para verificar antes de grabar el video

# Colores
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

echo -e "${BLUE}======================================"
echo "   TEST DE CONECTIVIDAD ENTRE NODOS"
echo "======================================${NC}"
echo ""

# Solicitar IPs
read -p "IP del Nodo 1 (PostgreSQL) [192.168.1.10]: " IP_DB
IP_DB=${IP_DB:-192.168.1.10}

read -p "IP del Nodo 2 (Backend) [192.168.1.20]: " IP_BACKEND
IP_BACKEND=${IP_BACKEND:-192.168.1.20}

read -p "IP del Nodo 3 (Frontend) [192.168.1.30]: " IP_FRONTEND
IP_FRONTEND=${IP_FRONTEND:-192.168.1.30}

echo ""
echo -e "${YELLOW}Probando conectividad...${NC}"
echo ""

# Test 1: PostgreSQL
echo -n "Test 1: PostgreSQL ($IP_DB:5432)... "
if timeout 3 bash -c "cat < /dev/null > /dev/tcp/$IP_DB/5432" 2>/dev/null; then
    echo -e "${GREEN}✓ OK${NC}"
    
    # Intentar consulta
    if psql -h $IP_DB -U postgres -d limpieza_empresas -c "SELECT 1;" &> /dev/null; then
        echo "         └─ Consulta SQL: ${GREEN}✓ OK${NC}"
    else
        echo "         └─ Consulta SQL: ${RED}✗ FALLO${NC}"
    fi
else
    echo -e "${RED}✗ NO ACCESIBLE${NC}"
fi
echo ""

# Test 2: Backend
echo -n "Test 2: Backend ($IP_BACKEND:5001)... "
if curl -s --max-time 3 http://$IP_BACKEND:5001/ > /dev/null; then
    echo -e "${GREEN}✓ OK${NC}"
    
    # Probar endpoint
    RESPONSE=$(curl -s http://$IP_BACKEND:5001/api/permisos)
    COUNT=$(echo $RESPONSE | grep -o "\[" | wc -l)
    if [ $COUNT -gt 0 ]; then
        echo "         └─ API Permisos: ${GREEN}✓ OK${NC}"
    fi
else
    echo -e "${RED}✗ NO ACCESIBLE${NC}"
fi
echo ""

# Test 3: Frontend
echo -n "Test 3: Frontend ($IP_FRONTEND:3001)... "
if curl -s --max-time 3 http://$IP_FRONTEND:3001/ > /dev/null; then
    echo -e "${GREEN}✓ OK${NC}"
else
    echo -e "${RED}✗ NO ACCESIBLE${NC}"
fi
echo ""

# Resumen
echo -e "${BLUE}======================================"
echo "   RESUMEN"
echo "======================================${NC}"
echo ""
echo "URLs para usar en el video:"
echo "  Frontend:  http://$IP_FRONTEND:3001"
echo "  Backend:   http://$IP_BACKEND:5001"
echo "  PostgreSQL: psql -h $IP_DB -U postgres -d limpieza_empresas"
echo ""
echo -e "${GREEN}¡Listo para grabar!${NC}"
echo ""

