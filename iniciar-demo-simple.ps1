# Script de Inicializacion para Demo
# Ejecutar: .\iniciar-demo-simple.ps1

Write-Host ""
Write-Host "=== INICIALIZACION PARA DEMO ===" -ForegroundColor Cyan
Write-Host ""

# Reiniciar Docker
Write-Host "Reiniciando Docker..." -ForegroundColor Yellow
docker compose down
docker compose up -d

# Esperar
Write-Host "Esperando 15 segundos..." -ForegroundColor Yellow
Start-Sleep -Seconds 15

# Cargar datos
Write-Host "Cargando datos de ejemplo..." -ForegroundColor Yellow
docker exec limpieza_backend python init_all_data.py

Write-Host ""
Write-Host "=== VERIFICACION ===" -ForegroundColor Cyan
Write-Host ""

# Docker
Write-Host "Estado de Docker:" -ForegroundColor Yellow
docker compose ps

Write-Host ""

# Obtener IP
$IP = (Get-NetIPAddress -AddressFamily IPv4 | Where-Object {$_.IPAddress -like "192.168.*"}).IPAddress | Select-Object -First 1
if (-not $IP) {
    $IP = (Get-NetIPAddress -AddressFamily IPv4 | Where-Object {$_.IPAddress -like "10.*"}).IPAddress | Select-Object -First 1
}
if (-not $IP) {
    $IP = "localhost"
}

Write-Host "Tu IP: $IP" -ForegroundColor Green
Write-Host ""

# Instrucciones
Write-Host "=== LISTO PARA DEMO ===" -ForegroundColor Green
Write-Host ""
Write-Host "COMPU 1 (este equipo):" -ForegroundColor Yellow
Write-Host "  1. Abrir PostgreSQL:" -ForegroundColor White
Write-Host "     docker exec -it limpieza_db psql -U postgres -d limpieza_empresas" -ForegroundColor Gray
Write-Host ""
Write-Host "COMPU 2 (otra maquina):" -ForegroundColor Yellow
Write-Host "  2. Abrir navegador en:" -ForegroundColor White
Write-Host "     http://${IP}:3001" -ForegroundColor Cyan
Write-Host ""

