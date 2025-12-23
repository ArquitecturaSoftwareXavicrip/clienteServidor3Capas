#!/bin/bash
# Script para inicializar datos en Docker

echo "Esperando a que PostgreSQL esté listo..."
sleep 5

echo "Cargando datos de ejemplo..."
docker exec limpieza_backend python /app/../database/init_db.py
docker exec limpieza_backend python /app/../database/init_permisos.py

echo "✅ Datos cargados correctamente"
echo ""
echo "🚀 Aplicación lista:"
echo "   Frontend: http://localhost:3001"
echo "   Backend:  http://localhost:5001"
echo ""

