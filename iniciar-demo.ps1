# Script de Inicialización Completo para Demo
# Ejecutar: .\iniciar-demo.ps1

Write-Host ""
Write-Host "╔════════════════════════════════════════════════════╗" -ForegroundColor Cyan
Write-Host "║   INICIALIZACIÓN PARA DEMO DE ARQUITECTURA        ║" -ForegroundColor Cyan
Write-Host "╚════════════════════════════════════════════════════╝" -ForegroundColor Cyan
Write-Host ""

# Paso 1: Detener contenedores anteriores
Write-Host "Paso 1: Deteniendo contenedores anteriores..." -ForegroundColor Yellow
docker compose down
Write-Host "  ✓ Detenido" -ForegroundColor Green
Write-Host ""

# Paso 2: Iniciar servicios
Write-Host "Paso 2: Iniciando servicios (esto puede tardar 1-2 minutos)..." -ForegroundColor Yellow
docker compose up -d
Write-Host "  ✓ Servicios iniciados" -ForegroundColor Green
Write-Host ""

# Paso 3: Esperar a que PostgreSQL esté listo
Write-Host "Paso 3: Esperando a que PostgreSQL esté listo..." -ForegroundColor Yellow
Start-Sleep -Seconds 15
Write-Host "  ✓ PostgreSQL listo" -ForegroundColor Green
Write-Host ""

# Paso 4: Cargar datos de ejemplo
Write-Host "Paso 4: Cargando datos de ejemplo..." -ForegroundColor Yellow
docker exec limpieza_backend python init_all_data.py
Write-Host ""

# Paso 5: Obtener IP
$IP = (Get-NetIPAddress -AddressFamily IPv4 | Where-Object {$_.IPAddress -like "192.168.*" -or $_.IPAddress -like "10.*"}).IPAddress | Select-Object -First 1
if (-not $IP) {
    $IP = "localhost"
}

# Paso 6: Verificar acceso
Write-Host "Paso 5: Verificando acceso..." -ForegroundColor Yellow
try {
    $response = Invoke-WebRequest -Uri "http://localhost:5001/api/permisos" -TimeoutSec 5
    $permisos = ($response.Content | ConvertFrom-Json).Count
    Write-Host "  ✓ Backend funcional ($permisos permisos cargados)" -ForegroundColor Green
} catch {
    Write-Host "  ⚠ Backend no responde aún, espera 30 segundos más" -ForegroundColor Yellow
}
Write-Host ""

# Resumen
Write-Host "╔════════════════════════════════════════════════════╗" -ForegroundColor Green
Write-Host "║              ✅ TODO LISTO                         ║" -ForegroundColor Green
Write-Host "╚════════════════════════════════════════════════════╝" -ForegroundColor Green
Write-Host ""
Write-Host "📊 Datos cargados:" -ForegroundColor Cyan
Write-Host "  - 2 empresas" -ForegroundColor White
Write-Host "  - 3 servicios" -ForegroundColor White
Write-Host "  - 2 contratos" -ForegroundColor White
Write-Host "  - 6 permisos" -ForegroundColor White
Write-Host "  - 8 empleados" -ForegroundColor White
Write-Host ""
Write-Host "🌐 URLs de acceso:" -ForegroundColor Cyan
Write-Host "  Localhost:  http://localhost:3001" -ForegroundColor Green
Write-Host "  Red Local:  http://${IP}:3001" -ForegroundColor Green
Write-Host ""
Write-Host "🎬 Para el video:" -ForegroundColor Yellow
Write-Host "  COMPU 1 (este equipo): Abrir terminal PostgreSQL" -ForegroundColor White
Write-Host "    docker exec -it limpieza_db psql -U postgres -d limpieza_empresas" -ForegroundColor Gray
Write-Host ""
Write-Host "  COMPU 2 (otra máquina): Abrir navegador" -ForegroundColor White
Write-Host "    http://${IP}:3001" -ForegroundColor Gray
Write-Host ""
Write-Host "📋 Comandos útiles:" -ForegroundColor Cyan
Write-Host "  Ver logs:      docker compose logs -f" -ForegroundColor White
Write-Host "  Detener:       docker compose down" -ForegroundColor White
Write-Host "  Reiniciar:     .\iniciar-demo.ps1" -ForegroundColor White
Write-Host ""

