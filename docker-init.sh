#!/bin/bash
# Script para inicializar datos en Docker

echo "Esperando a que PostgreSQL esté listo..."
sleep 10

echo "Cargando datos de ejemplo..."
docker exec limpieza_backend python init_all_data.py

echo ""
echo "✅ Datos cargados correctamente"
echo ""
echo "🚀 Aplicación lista:"
echo "   Frontend: http://localhost:3001"
echo "   Backend:  http://localhost:5001"
echo ""

