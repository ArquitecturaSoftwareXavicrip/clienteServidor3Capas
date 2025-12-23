# 🚀 Quick Start - Módulo de Permisos

## ⚡ Inicio Rápido en 3 Pasos

### 1️⃣ Ejecutar con Docker (Recomendado)

```bash
# Construir y ejecutar
docker compose up --build -d

# Esperar 10 segundos...

# Cargar datos de ejemplo
docker exec -it limpieza_backend python /app/../database/init_permisos.py

# Abrir navegador
# http://localhost:3001
# Hacer clic en "Permisos"
```

**✅ ¡Listo! El módulo está funcionando.**

---

### 2️⃣ Ejecutar Manualmente (Windows PowerShell)

```powershell
# Terminal 1 - Backend
cd backend
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
$env:PORT=5001; python run.py

# Terminal 2 - Cargar datos de ejemplo
cd database
python init_permisos.py

# Terminal 3 - Frontend
cd frontend
npm install
$env:PORT=3001; npm start

# Abrir http://localhost:3001
```

---

### 3️⃣ Verificar Funcionamiento

1. **Abrir navegador** en `http://localhost:3001`
2. **Hacer clic** en el botón "Permisos" en la navegación
3. **Ver datos de ejemplo** en la tabla
4. **Probar crear** un nuevo permiso

---

## 🧪 Pruebas Rápidas

### Crear un Permiso

```javascript
// En el formulario web:
Empleado: "Pedro Sánchez"
Fecha Inicio: "2024-02-01"
Fecha Fin: "2024-02-10"
Días: 9
Observaciones: "Vacaciones familiares"

[Clic en Crear]
```

### Filtrar por Estado

```javascript
// En el selector de filtro:
Seleccionar: "Pendientes"
// La tabla mostrará solo permisos pendientes
```

### Aprobar un Permiso

```javascript
// En la tabla, para un permiso pendiente:
[Clic en Aprobar]
// Confirmar
// El estado cambiará a 🟢 APROBADO
```

---

## 🔍 Verificar API (cURL)

### Obtener todos los permisos

```bash
curl http://localhost:5001/api/permisos
```

### Crear permiso

```bash
curl -X POST http://localhost:5001/api/permisos \
  -H "Content-Type: application/json" \
  -d '{
    "empleado": "Test User",
    "tipo": "Vacaciones",
    "fecha_inicio": "2024-03-01",
    "fecha_fin": "2024-03-10",
    "dias_solicitados": 9,
    "observaciones": "Prueba desde cURL"
  }'
```

### Filtrar pendientes

```bash
curl http://localhost:5001/api/permisos?estado=pendiente
```

### Aprobar permiso

```bash
curl -X POST http://localhost:5001/api/permisos/1/aprobar \
  -H "Content-Type: application/json" \
  -d '{"observaciones": "Aprobado por gerencia"}'
```

---

## 📱 Interfaz Web

La interfaz incluye:

- ✅ **Formulario**: Crear/editar permisos
- ✅ **Tabla**: Ver todos los permisos
- ✅ **Filtros**: Por estado (Todos, Pendientes, Aprobados, Rechazados)
- ✅ **Acciones**: Aprobar, Rechazar, Editar, Eliminar
- ✅ **Estados con color**: 🟡 Pendiente, 🟢 Aprobado, 🔴 Rechazado

---

## 🎯 Datos de Ejemplo

El script `init_permisos.py` crea 6 permisos de ejemplo:

| Empleado | Días | Estado | Descripción |
|----------|------|--------|-------------|
| Juan Pérez | 7 | 🟡 Pendiente | Vacaciones futuras |
| María García | 14 | 🟡 Pendiente | Viaje familiar |
| Carlos Rodríguez | 5 | 🟢 Aprobado | Ya tomadas |
| Ana Martínez | 14 | 🟢 Aprobado | Fin de año |
| Luis Fernández | 7 | 🔴 Rechazado | Sin cobertura |
| Carmen López | 4 | 🟡 Pendiente | Fin de semana largo |

---

## 🐛 Troubleshooting

### Puerto ocupado (Windows)

```powershell
# Ver qué proceso usa el puerto
netstat -ano | findstr :5001
netstat -ano | findstr :3001

# Matar proceso
taskkill /PID <PID> /F
```

### Docker no inicia

```bash
# Ver logs
docker compose logs backend
docker compose logs frontend

# Reconstruir
docker compose down -v
docker compose up --build
```

### Frontend no conecta con backend

1. Verificar que backend esté corriendo: `http://localhost:5001`
2. Verificar CORS en `backend/app/__init__.py`
3. Verificar `REACT_APP_API_URL` en `frontend/.env`

---

## 📚 Documentación Completa

Para más detalles:

- 📖 [MODULO_PERMISOS.md](MODULO_PERMISOS.md) - Documentación técnica
- 🏗️ [ESTRUCTURA_MODULO_PERMISOS.md](ESTRUCTURA_MODULO_PERMISOS.md) - Estructura del código
- ✅ [IMPLEMENTACION_PERMISOS.md](IMPLEMENTACION_PERMISOS.md) - Guía de implementación
- 📋 [README.md](README.md) - Información general del proyecto

---

## 🎉 ¡Eso es todo!

En menos de 5 minutos deberías tener el módulo funcionando.

**¿Problemas?** Revisa los logs:

```bash
# Docker
docker compose logs -f backend
docker compose logs -f frontend

# Manual
# Ver consola donde ejecutaste backend/frontend
```

---

**💡 Tip**: Si quieres agregar más permisos de ejemplo, edita `database/init_permisos.py` y vuelve a ejecutarlo.

