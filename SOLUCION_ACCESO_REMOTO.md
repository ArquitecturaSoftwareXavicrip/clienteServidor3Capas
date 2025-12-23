# 🔧 Solución: Acceso Remoto desde Otra Computadora

## ✅ Pasos para Resolver

---

## 1️⃣ Reiniciar Docker con Nueva Configuración

```powershell
# Detener Docker
docker compose down

# Iniciar con la nueva configuración (CORS = *)
docker compose up -d

# Esperar
Start-Sleep -Seconds 15
```

---

## 2️⃣ Cargar Datos con el Nuevo Script

```powershell
# Usar el script que funciona en Docker
docker exec limpieza_backend python init_all_data.py
```

**Deberías ver:**
```
✓ 2 empresas creadas
✓ 3 servicios creados
✓ 2 contratos creados
✓ 6 permisos creados
✓ 8 empleados creados
```

---

## 3️⃣ Verificar que los Datos se Cargaron

```powershell
# Debe devolver 6 permisos (no [])
curl http://localhost:5001/api/permisos

# Debe devolver 8 empleados
curl http://localhost:5001/api/empleados
```

---

## 4️⃣ Obtener tu IP

```powershell
ipconfig | findstr IPv4
```

Busca algo como:
```
Dirección IPv4. . . . . . . . . . . . : 192.168.1.20
```

**Anota tu IP:** _______________

---

## 5️⃣ Verificar Acceso desde tu Propia IP

```powershell
# Reemplaza 192.168.1.20 con TU IP real

# Probar backend
curl http://192.168.1.20:5001/

# Probar API
curl http://192.168.1.20:5001/api/permisos

# Probar frontend
curl http://192.168.1.20:3001/
```

**Si alguno falla con tu propia IP** → El firewall está bloqueando

---

## 6️⃣ Verificar Reglas de Firewall

```powershell
Get-NetFirewallRule | Where-Object {$_.DisplayName -like "*Demo*"} | Format-Table DisplayName, Enabled, Action
```

**Debe mostrar:**
```
DisplayName          Enabled Action
-----------          ------- ------
Backend Flask Demo   True    Allow
Frontend React Demo  True    Allow
```

**Si no aparecen o están Disabled** → Crear las reglas (ver paso 7)

---

## 7️⃣ Crear Reglas de Firewall (Si Faltan)

**Ejecutar PowerShell como Administrador:**

```powershell
# Abrir puertos
New-NetFirewallRule -DisplayName "Backend Flask Demo" -Direction Inbound -LocalPort 5001 -Protocol TCP -Action Allow -Profile Any

New-NetFirewallRule -DisplayName "Frontend React Demo" -Direction Inbound -LocalPort 3001 -Protocol TCP -Action Allow -Profile Any

Write-Host "✅ Puertos abiertos en Firewall" -ForegroundColor Green
```

---

## 8️⃣ Verificar Puertos Escuchando en 0.0.0.0

```powershell
netstat -ano | findstr :5001
netstat -ano | findstr :3001
```

**CORRECTO:**
```
TCP    0.0.0.0:5001    0.0.0.0:0    LISTENING
TCP    0.0.0.0:3001    0.0.0.0:0    LISTENING
```

**INCORRECTO:**
```
TCP    127.0.0.1:5001    0.0.0.0:0    LISTENING
```

Si ves `127.0.0.1`, el docker-compose.yml no se actualizó correctamente.

---

## 9️⃣ Desde COMPU 2: Probar Acceso

```powershell
# Reemplaza con la IP real de COMPU 1

# Test 1: Ping
ping 192.168.1.20
# Debe responder ✓

# Test 2: Backend
curl http://192.168.1.20:5001/
# Debe devolver JSON ✓

# Test 3: API
curl http://192.168.1.20:5001/api/permisos
# Debe devolver array con 6 permisos ✓

# Test 4: Frontend
curl http://192.168.1.20:3001/
# Debe devolver HTML ✓

# Test 5: Abrir navegador
Start-Process "http://192.168.1.20:3001"
```

---

## ✅ Script TODO-EN-UNO

Ejecuta esto en **COMPU 1**:

```powershell
# ========== REINICIAR Y CONFIGURAR ==========
docker compose down
docker compose up -d
Start-Sleep -Seconds 15
docker exec limpieza_backend python init_all_data.py

# ========== OBTENER IP ==========
$IP = (Get-NetIPAddress -AddressFamily IPv4 | Where-Object {$_.IPAddress -like "192.168.*"}).IPAddress | Select-Object -First 1
if (-not $IP) { $IP = "localhost" }

# ========== VERIFICACIÓN ==========
Write-Host ""
Write-Host "=== VERIFICACIÓN ===" -ForegroundColor Cyan
Write-Host ""

# Test 1: Docker
Write-Host "Docker:" -ForegroundColor Yellow
docker compose ps | Select-String "Up"
Write-Host ""

# Test 2: Datos cargados
Write-Host "Datos:" -ForegroundColor Yellow
$permisos = (Invoke-WebRequest -Uri "http://localhost:5001/api/permisos").Content | ConvertFrom-Json
Write-Host "  Permisos: $($permisos.Count)" -ForegroundColor Green

$empleados = (Invoke-WebRequest -Uri "http://localhost:5001/api/empleados").Content | ConvertFrom-Json
Write-Host "  Empleados: $($empleados.Count)" -ForegroundColor Green
Write-Host ""

# Test 3: Firewall
Write-Host "Firewall:" -ForegroundColor Yellow
$rules = Get-NetFirewallRule | Where-Object {$_.DisplayName -like "*Demo*"}
if ($rules.Count -ge 2) {
    Write-Host "  ✓ Reglas configuradas" -ForegroundColor Green
} else {
    Write-Host "  ⚠ Falta configurar reglas" -ForegroundColor Yellow
    Write-Host "  Ejecuta como Administrador:" -ForegroundColor Red
    Write-Host '  New-NetFirewallRule -DisplayName "Backend Flask Demo" -Direction Inbound -LocalPort 5001 -Protocol TCP -Action Allow' -ForegroundColor Gray
    Write-Host '  New-NetFirewallRule -DisplayName "Frontend React Demo" -Direction Inbound -LocalPort 3001 -Protocol TCP -Action Allow' -ForegroundColor Gray
}
Write-Host ""

# Test 4: Acceso externo
Write-Host "Acceso desde red:" -ForegroundColor Yellow
try {
    Invoke-WebRequest -Uri "http://${IP}:5001/" -TimeoutSec 3 | Out-Null
    Write-Host "  ✓ Backend accesible desde $IP" -ForegroundColor Green
} catch {
    Write-Host "  ✗ Backend NO accesible (verificar firewall)" -ForegroundColor Red
}

try {
    Invoke-WebRequest -Uri "http://${IP}:3001/" -TimeoutSec 3 | Out-Null
    Write-Host "  ✓ Frontend accesible desde $IP" -ForegroundColor Green
} catch {
    Write-Host "  ✗ Frontend NO accesible (verificar firewall)" -ForegroundColor Red
}
Write-Host ""

# ========== RESULTADO ==========
Write-Host "╔════════════════════════════════════════════════════╗" -ForegroundColor Green
Write-Host "║              🎬 LISTO PARA GRABAR                  ║" -ForegroundColor Green
Write-Host "╚════════════════════════════════════════════════════╝" -ForegroundColor Green
Write-Host ""
Write-Host "📍 Tu IP: $IP" -ForegroundColor Cyan
Write-Host ""
Write-Host "🖥️  COMPU 1 (este equipo):" -ForegroundColor Yellow
Write-Host "   Abrir terminal PostgreSQL:" -ForegroundColor White
Write-Host "   .\monitor-bd.ps1" -ForegroundColor Cyan
Write-Host ""
Write-Host "💻 COMPU 2 (otra máquina):" -ForegroundColor Yellow
Write-Host "   Abrir navegador en:" -ForegroundColor White
Write-Host "   http://${IP}:3001" -ForegroundColor Cyan
Write-Host ""
Write-Host "📚 Ver guión del video: DEMO_VIDEO_GUION.md" -ForegroundColor Gray
Write-Host ""

