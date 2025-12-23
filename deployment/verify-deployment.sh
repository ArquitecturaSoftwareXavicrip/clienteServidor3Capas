#!/bin/bash
# Deployment Verification Script
# Este script verifica que todos los nodos están correctamente configurados

set -e

# Colores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

# Variables de configuración
NODE1_IP="192.168.1.10"
NODE2_IP="192.168.1.20"
NODE3_IP="192.168.1.30"
DB_PORT="5432"
BACKEND_PORT="5001"
FRONTEND_PORT="3001"

# Contadores
PASSED=0
FAILED=0

# Función para imprimir resultados
print_result() {
    if [ $1 -eq 0 ]; then
        echo -e "${GREEN}✓${NC} $2"
        ((PASSED++))
    else
        echo -e "${RED}✗${NC} $2"
        ((FAILED++))
    fi
}

echo "╔════════════════════════════════════════════════════════════╗"
echo "║    Verificación de Despliegue en 3 Nodos                  ║"
echo "╚════════════════════════════════════════════════════════════╝"
echo ""

# ============================================================
# VERIFICACIONES DE NODE 1 (DATABASE)
# ============================================================
echo -e "${YELLOW}=== Node 1: Database (Tier 3) ===${NC}"

# Verificar conectividad
ping -c 1 $NODE1_IP &> /dev/null
print_result $? "Conectividad con Node 1"

# Verificar PostgreSQL corriendo
ssh -o ConnectTimeout=5 usuario@$NODE1_IP "sudo systemctl is-active postgresql" &> /dev/null
print_result $? "PostgreSQL está corriendo"

# Verificar que escucha en el puerto
ssh -o ConnectTimeout=5 usuario@$NODE1_IP "sudo netstat -tulpn | grep 5432" &> /dev/null
print_result $? "PostgreSQL escucha en puerto 5432"

# Verificar base de datos
ssh -o ConnectTimeout=5 usuario@$NODE1_IP "psql -h localhost -U limpieza_user -d limpieza_empresas -c 'SELECT 1'" &> /dev/null
print_result $? "Base de datos limpieza_empresas accesible"

# Verificar tablas
ssh -o ConnectTimeout=5 usuario@$NODE1_IP "psql -h localhost -U limpieza_user -d limpieza_empresas -c '\dt'" | grep -q "empresas"
print_result $? "Tabla 'empresas' existe"

ssh -o ConnectTimeout=5 usuario@$NODE1_IP "psql -h localhost -U limpieza_user -d limpieza_empresas -c '\dt'" | grep -q "servicios"
print_result $? "Tabla 'servicios' existe"

ssh -o ConnectTimeout=5 usuario@$NODE1_IP "psql -h localhost -U limpieza_user -d limpieza_empresas -c '\dt'" | grep -q "contratos"
print_result $? "Tabla 'contratos' existe"

# Verificar firewall
ssh -o ConnectTimeout=5 usuario@$NODE1_IP "sudo ufw status | grep 5432" &> /dev/null
print_result $? "Firewall permite puerto 5432"

echo ""

# ============================================================
# VERIFICACIONES DE NODE 2 (BACKEND)
# ============================================================
echo -e "${YELLOW}=== Node 2: Backend (Tier 2) ===${NC}"

# Verificar conectividad
ping -c 1 $NODE2_IP &> /dev/null
print_result $? "Conectividad con Node 2"

# Verificar Backend corriendo
ssh -o ConnectTimeout=5 usuario@$NODE2_IP "sudo systemctl is-active limpieza-backend" &> /dev/null
print_result $? "Backend está corriendo"

# Verificar que escucha en el puerto
ssh -o ConnectTimeout=5 usuario@$NODE2_IP "sudo netstat -tulpn | grep 5001" &> /dev/null
print_result $? "Backend escucha en puerto 5001"

# Verificar respuesta HTTP
curl -s http://$NODE2_IP:$BACKEND_PORT/ | grep -q "API de Servicios"
print_result $? "Backend responde a solicitudes HTTP"

# Verificar archivo .env
ssh -o ConnectTimeout=5 usuario@$NODE2_IP "test -f /opt/limpieza/arqCS-NCapas/backend/.env"
print_result $? "Archivo .env existe"

# Verificar conexión a base de datos desde backend
ssh -o ConnectTimeout=5 usuario@$NODE2_IP "psql -h $NODE1_IP -U limpieza_user -d limpieza_empresas -c 'SELECT 1'" &> /dev/null
print_result $? "Backend puede conectar a base de datos"

# Verificar firewall
ssh -o ConnectTimeout=5 usuario@$NODE2_IP "sudo ufw status | grep 5001" &> /dev/null
print_result $? "Firewall permite puerto 5001"

echo ""

# ============================================================
# VERIFICACIONES DE NODE 3 (FRONTEND)
# ============================================================
echo -e "${YELLOW}=== Node 3: Frontend (Tier 1) ===${NC}"

# Verificar conectividad
ping -c 1 $NODE3_IP &> /dev/null
print_result $? "Conectividad con Node 3"

# Verificar Nginx corriendo
ssh -o ConnectTimeout=5 usuario@$NODE3_IP "sudo systemctl is-active nginx" &> /dev/null
print_result $? "Nginx está corriendo"

# Verificar que escucha en el puerto
ssh -o ConnectTimeout=5 usuario@$NODE3_IP "sudo netstat -tulpn | grep 3001" &> /dev/null
print_result $? "Nginx escucha en puerto 3001"

# Verificar respuesta HTTP
curl -s http://$NODE3_IP:$FRONTEND_PORT/ | grep -q "html"
print_result $? "Frontend responde a solicitudes HTTP"

# Verificar archivo .env
ssh -o ConnectTimeout=5 usuario@$NODE3_IP "test -f /opt/limpieza/arqCS-NCapas/frontend/.env"
print_result $? "Archivo .env existe"

# Verificar build
ssh -o ConnectTimeout=5 usuario@$NODE3_IP "test -d /opt/limpieza/arqCS-NCapas/frontend/build"
print_result $? "Build de producción existe"

# Verificar firewall
ssh -o ConnectTimeout=5 usuario@$NODE3_IP "sudo ufw status | grep 3001" &> /dev/null
print_result $? "Firewall permite puerto 3001"

echo ""

# ============================================================
# VERIFICACIONES DE CONECTIVIDAD ENTRE NODOS
# ============================================================
echo -e "${YELLOW}=== Conectividad entre Nodos ===${NC}"

# Node 2 -> Node 1
ssh -o ConnectTimeout=5 usuario@$NODE2_IP "psql -h $NODE1_IP -U limpieza_user -d limpieza_empresas -c 'SELECT version()'" &> /dev/null
print_result $? "Node 2 puede conectar a Node 1 (Database)"

# Node 3 -> Node 2
curl -s http://$NODE2_IP:$BACKEND_PORT/api/empresas &> /dev/null
print_result $? "Node 3 puede conectar a Node 2 (Backend)"

echo ""

# ============================================================
# RESUMEN
# ============================================================
TOTAL=$((PASSED + FAILED))
PERCENTAGE=$((PASSED * 100 / TOTAL))

echo "╔════════════════════════════════════════════════════════════╗"
echo "║                      RESUMEN                               ║"
echo "╠════════════════════════════════════════════════════════════╣"
echo -e "║ Pruebas Pasadas:  ${GREEN}${PASSED}${NC}                                        ║"
echo -e "║ Pruebas Fallidas: ${RED}${FAILED}${NC}                                        ║"
echo -e "║ Porcentaje:       ${PERCENTAGE}%                                      ║"
echo "╚════════════════════════════════════════════════════════════╝"

if [ $FAILED -eq 0 ]; then
    echo -e "\n${GREEN}✓ Despliegue verificado exitosamente${NC}"
    exit 0
else
    echo -e "\n${RED}✗ Hay problemas que necesitan ser resueltos${NC}"
    exit 1
fi
