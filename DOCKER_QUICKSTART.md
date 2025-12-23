# 🐳 Guía Rápida: Ejecutar con Docker

## 🚀 Inicio Rápido

### Paso 1: Ejecutar Docker Compose

```powershell
# Construir y ejecutar todos los servicios
docker compose up --build -d

# Ver logs
docker compose logs -f
```

### Paso 2: Cargar Datos de Ejemplo

**Opción A: Usar el script (Linux/Mac/Git Bash)**

```bash
chmod +x docker-init.sh
./docker-init.sh
```

**Opción B: Manualmente (Windows PowerShell)**

```powershell
# Esperar 10 segundos para que PostgreSQL esté listo
Start-Sleep -Seconds 10

# Cargar datos
docker exec limpieza_backend python ../database/init_db.py
docker exec limpieza_backend python ../database/init_permisos.py
```

### Paso 3: Abrir la Aplicación

Abrir en el navegador: **http://localhost:3001**

---

## 📊 Servicios Disponibles

| Servicio | URL | Descripción |
|----------|-----|-------------|
| Frontend | http://localhost:3001 | Aplicación React |
| Backend API | http://localhost:5001 | API RESTful |
| PostgreSQL | localhost:5432 | Base de datos |

---

## 🛠️ Comandos Útiles

### Ver Logs

```powershell
# Todos los servicios
docker compose logs -f

# Solo backend
docker compose logs -f backend

# Solo frontend
docker compose logs -f frontend

# Solo database
docker compose logs -f database
```

### Detener Servicios

```powershell
# Detener
docker compose down

# Detener y eliminar volúmenes (borra la BD)
docker compose down -v
```

### Reiniciar un Servicio

```powershell
# Reiniciar backend
docker compose restart backend

# Reiniciar frontend
docker compose restart frontend

# Reiniciar database
docker compose restart database
```

### Reconstruir Servicios

```powershell
# Reconstruir todo
docker compose up --build

# Reconstruir solo backend
docker compose up --build backend

# Reconstruir solo frontend
docker compose up --build frontend
```

### Ejecutar Comandos en Contenedores

```powershell
# Abrir shell en backend
docker exec -it limpieza_backend bash

# Abrir shell en frontend
docker exec -it limpieza_frontend sh

# Conectar a PostgreSQL
docker exec -it limpieza_db psql -U postgres -d limpieza_empresas
```

---

## 🔍 Verificar que Todo Funciona

### Backend

```powershell
curl http://localhost:5001/
curl http://localhost:5001/api/empresas
curl http://localhost:5001/api/permisos
```

### PostgreSQL

```powershell
# Conectar a la base de datos
docker exec -it limpieza_db psql -U postgres -d limpieza_empresas

# Dentro de psql:
SELECT COUNT(*) FROM empresas;
SELECT COUNT(*) FROM servicios;
SELECT COUNT(*) FROM contratos;
SELECT COUNT(*) FROM permisos;
\q
```

### Frontend

Abrir: http://localhost:3001

- Verificar que carga
- Hacer clic en "Permisos"
- Ver los 6 permisos de ejemplo
- Crear un nuevo permiso

---

## 🐛 Solución de Problemas

### Error: "port is already allocated"

```powershell
# Ver qué proceso usa el puerto
netstat -ano | findstr :5001
netstat -ano | findstr :3001

# Matar el proceso
taskkill /PID <PID> /F

# O cambiar puerto en docker-compose.yml
```

### Error: "network not found"

```powershell
docker compose down
docker network prune
docker compose up --build
```

### Frontend no carga

```powershell
# Ver logs
docker compose logs frontend

# Reconstruir
docker compose down
docker compose up --build frontend
```

### Backend no conecta a PostgreSQL

```powershell
# Ver logs
docker compose logs backend
docker compose logs database

# Reiniciar todo
docker compose down
docker compose up --build
```

### Limpiar Todo y Empezar de Nuevo

```powershell
# Detener y eliminar todo
docker compose down -v

# Limpiar imágenes y contenedores
docker system prune -a

# Reconstruir
docker compose up --build -d
```

---

## 📦 Arquitectura Docker

```
┌─────────────────────────────────────────────────┐
│              Docker Network                     │
│                                                 │
│  ┌──────────────────┐                          │
│  │  PostgreSQL      │  Tier 3: Base de Datos   │
│  │  Container       │  Puerto: 5432            │
│  │  limpieza_db     │  Sin contraseña (trust)  │
│  └────────┬─────────┘                          │
│           │                                     │
│           │ SQL                                 │
│           ▼                                     │
│  ┌──────────────────┐                          │
│  │  Flask Backend   │  Tier 2: API             │
│  │  Container       │  Puerto: 5001            │
│  │  limpieza_backend│  Python 3.11             │
│  └────────┬─────────┘                          │
│           │                                     │
│           │ HTTP/REST                           │
│           ▼                                     │
│  ┌──────────────────┐                          │
│  │  React Frontend  │  Tier 1: UI              │
│  │  Container       │  Puerto: 3001            │
│  │  limpieza_frontend│ Node.js 18              │
│  └──────────────────┘                          │
│                                                 │
└─────────────────────────────────────────────────┘
         ↓
    Host Machine
    localhost:3001 → Frontend
    localhost:5001 → Backend
```

---

## ✅ Checklist de Docker

- [ ] Docker Desktop instalado y corriendo
- [ ] `docker compose up --build -d` ejecutado
- [ ] Datos de ejemplo cargados
- [ ] Frontend accesible en http://localhost:3001
- [ ] Backend accesible en http://localhost:5001
- [ ] PostgreSQL corriendo (verificar con `docker compose ps`)
- [ ] Módulo de Permisos funcional

---

## 🎯 Ventajas de Docker

✅ **No necesitas instalar:**
- PostgreSQL
- Python
- Node.js

✅ **Ambiente consistente:**
- Funciona igual en Windows, Mac y Linux

✅ **Fácil de limpiar:**
- `docker compose down -v` elimina todo

✅ **Múltiples ambientes:**
- Desarrollo y producción separados

---

## 📚 Recursos

- Documentación de Docker: https://docs.docker.com/
- Docker Compose: https://docs.docker.com/compose/
- PostgreSQL en Docker: https://hub.docker.com/_/postgres

---

**¡Disfruta de tu aplicación en Docker!** 🐳🚀

