#!/bin/bash
# Script para monitorear la base de datos en tiempo real
# Útil para demostración en video

# Colores
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
NC='\033[0m'

echo -e "${CYAN}======================================"
echo "   MONITOR EN TIEMPO REAL"
echo "   Base de Datos: limpieza_empresas"
echo "======================================${NC}"
echo ""
echo "Presiona Ctrl+C para salir"
echo ""

# Leer IP de PostgreSQL
read -p "IP de PostgreSQL [localhost]: " DB_HOST
DB_HOST=${DB_HOST:-localhost}

while true; do
    clear
    echo -e "${CYAN}╔════════════════════════════════════════════════════╗"
    echo "║     MONITOR DE PERMISOS EN TIEMPO REAL             ║"
    echo "╚════════════════════════════════════════════════════╝${NC}"
    echo ""
    echo -e "${YELLOW}Hora: $(date '+%Y-%m-%d %H:%M:%S')${NC}"
    echo -e "${YELLOW}PostgreSQL: $DB_HOST${NC}"
    echo ""
    
    # Resumen por estado
    echo -e "${GREEN}📊 RESUMEN POR ESTADO:${NC}"
    psql -h $DB_HOST -U postgres -d limpieza_empresas -t -A -c "
    SELECT 
        CASE 
            WHEN estado = 'pendiente' THEN '🟡 Pendiente'
            WHEN estado = 'aprobado' THEN '🟢 Aprobado'
            WHEN estado = 'rechazado' THEN '🔴 Rechazado'
        END as estado,
        COUNT(*) as cantidad
    FROM permisos 
    GROUP BY estado 
    ORDER BY estado;"
    echo ""
    
    # Últimos 5 permisos
    echo -e "${BLUE}📋 ÚLTIMOS 5 PERMISOS:${NC}"
    psql -h $DB_HOST -U postgres -d limpieza_empresas -c "
    SELECT 
        id as ID,
        LEFT(empleado, 20) as Empleado,
        estado as Estado,
        dias_solicitados as Días,
        TO_CHAR(fecha_inicio, 'DD/MM/YYYY') as Inicio
    FROM permisos 
    ORDER BY id DESC 
    LIMIT 5;"
    
    echo ""
    echo -e "${CYAN}Actualizando cada 2 segundos...${NC}"
    sleep 2
done

