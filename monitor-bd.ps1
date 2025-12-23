# Script para monitorear PostgreSQL en tiempo real
# Útil para el video de demostración

Write-Host ""
Write-Host "╔════════════════════════════════════════════════════╗" -ForegroundColor Cyan
Write-Host "║      MONITOR DE BASE DE DATOS EN TIEMPO REAL      ║" -ForegroundColor Cyan
Write-Host "╚════════════════════════════════════════════════════╝" -ForegroundColor Cyan
Write-Host ""
Write-Host "Este script abrirá PostgreSQL para que puedas consultar" -ForegroundColor Yellow
Write-Host "la base de datos en tiempo real durante el video." -ForegroundColor Yellow
Write-Host ""
Write-Host "Comandos SQL útiles:" -ForegroundColor Cyan
Write-Host "  SELECT * FROM permisos ORDER BY id;" -ForegroundColor Gray
Write-Host "  SELECT COUNT(*) FROM permisos;" -ForegroundColor Gray
Write-Host "  SELECT id, empleado, estado FROM permisos ORDER BY id DESC LIMIT 5;" -ForegroundColor Gray
Write-Host "  \q   (para salir)" -ForegroundColor Gray
Write-Host ""
Write-Host "Presiona Enter para abrir PostgreSQL..." -ForegroundColor Yellow
Read-Host

# Abrir PostgreSQL
docker exec -it limpieza_db psql -U postgres -d limpieza_empresas

