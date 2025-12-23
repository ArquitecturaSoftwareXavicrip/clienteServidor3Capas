# 🖥️ Guía de Inicio Local - Windows

## ✅ Pasos Completos para Ejecutar Sin Docker

---

## 📋 Paso 1: Configurar PostgreSQL

### A) Verificar PostgreSQL

```powershell
# Verificar instalación
psql --version

# Si no está, descargar de:
# https://www.postgresql.org/download/windows/
```

### B) Crear Base de Datos

```powershell
# Conectar a PostgreSQL
psql -U postgres

# Dentro de psql:
CREATE DATABASE limpieza_empresas;
\l
\q
```

### C) Crear Tablas

```powershell
cd "C:\Users\samuc\OneDrive\Escritorio\uni\7mo ciclo\software\clienteServidor3Capas\database"

psql -U postgres -d limpieza_empresas -f schema.sql
```

**Verificar:**
```powershell
psql -U postgres -d limpieza_empresas -c "\dt"

# Deberías ver:
# empresas
# servicios
# contratos
# permisos
# empleados
```

---

## 🐍 Paso 2: Configurar Backend

### A) Navegar a Backend

```powershell
cd "C:\Users\samuc\OneDrive\Escritorio\uni\7mo ciclo\software\clienteServidor3Capas\backend"
```

### B) Crear Archivo .env

```powershell
@"
FLASK_ENV=development
PORT=5001
SECRET_KEY=dev-secret-key-cambiar-en-produccion

SQLALCHEMY_DATABASE_URI=postgresql://postgres@localhost:5432/limpieza_empresas

CORS_ORIGINS=http://localhost:3001,http://localhost:3000
"@ | Out-File -FilePath .env -Encoding utf8

# Verificar
Get-Content .env
```

### C) Crear Entorno Virtual e Instalar

```powershell
# Crear venv
python -m venv venv

# Activar (puede requerir permisos)
.\venv\Scripts\Activate.ps1

# Si hay error de permisos:
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser

# Volver a activar
.\venv\Scripts\Activate.ps1

# Actualizar pip
python -m pip install --upgrade pip

# Instalar dependencias
pip install -r requirements.txt
pip install psycopg2-binary
```

### D) Cargar Datos de Ejemplo

```powershell
# Con el venv activado
cd ..\database

python init_db.py
python init_permisos.py
python init_empleados.py

# Deberías ver mensajes de éxito para cada uno
cd ..\backend
```

### E) Ejecutar Backend

```powershell
# Con el venv activado
python run.py

# Deberías ver:
#  * Running on http://127.0.0.1:5001
#  * Running on http://192.168.x.x:5001
```

**✅ Backend corriendo en:** http://localhost:5001

**MANTÉN ESTA TERMINAL ABIERTA**

---

## ⚛️ Paso 3: Configurar Frontend

### A) Abrir NUEVA Terminal PowerShell

(Deja la anterior corriendo con el backend)

### B) Navegar a Frontend

```powershell
cd "C:\Users\samuc\OneDrive\Escritorio\uni\7mo ciclo\software\clienteServidor3Capas\frontend"
```

### C) Crear Archivo .env

```powershell
@"
REACT_APP_API_URL=http://localhost:5001/api
PORT=3001
"@ | Out-File -FilePath .env -Encoding utf8

# Verificar
Get-Content .env
```

### D) Instalar Dependencias

```powershell
npm install
```

### E) Ejecutar Frontend

```powershell
npm start
```

**Se abrirá automáticamente el navegador en:** http://localhost:3001

**MANTÉN ESTA TERMINAL ABIERTA**

---

## 🎯 Paso 4: Probar la Aplicación

### En el Navegador (http://localhost:3001):

#### 1️⃣ Empresas
- Ver 2 empresas de ejemplo
- Crear una nueva empresa

#### 2️⃣ Servicios
- Ver 3 servicios de ejemplo
- Crear un nuevo servicio

#### 3️⃣ Contratos
- Ver 2 contratos de ejemplo
- Crear un nuevo contrato

#### 4️⃣ **Permisos** 🆕
- Ver 6 permisos de ejemplo
- Estados con colores: 🟡 Pendiente, 🟢 Aprobado, 🔴 Rechazado
- Crear un nuevo permiso
- Aprobar un permiso pendiente
- Rechazar un permiso
- Filtrar por estado

#### 5️⃣ **Empleados** 🆕
- Ver 8 empleados de ejemplo
- Diferentes cargos (Gerente, Supervisor, Operario, etc.)
- Crear un nuevo empleado
- Editar empleado existente

---

## ✅ Verificar en la Base de Datos

```powershell
# Abrir TERCERA terminal
psql -U postgres -d limpieza_empresas

# Dentro de psql, consultar:
SELECT COUNT(*) FROM empresas;    -- 2
SELECT COUNT(*) FROM servicios;   -- 3
SELECT COUNT(*) FROM contratos;   -- 2
SELECT COUNT(*) FROM permisos;    -- 6
SELECT COUNT(*) FROM empleados;   -- 8

# Ver datos específicos:
SELECT * FROM permisos ORDER BY estado;
SELECT * FROM empleados ORDER BY cargo;

# Salir:
\q
```

---

## 🐛 Solución de Problemas

### Error: "psql: command not found"

PostgreSQL no está en el PATH:

```powershell
# Agregar al PATH temporalmente
$env:Path += ";C:\Program Files\PostgreSQL\15\bin"

# Verificar
psql --version
```

### Error: "password authentication failed"

Configurar trust en `pg_hba.conf`:

```powershell
# Ubicación (ajustar versión):
notepad "C:\Program Files\PostgreSQL\15\data\pg_hba.conf"

# Cambiar:
host    all    all    127.0.0.1/32    md5
# Por:
host    all    all    127.0.0.1/32    trust

# Reiniciar PostgreSQL en Servicios de Windows
```

### Error: "database does not exist"

```powershell
psql -U postgres -c "CREATE DATABASE limpieza_empresas;"
```

### Error: Backend no conecta a PostgreSQL

Verificar archivo `.env`:
```powershell
Get-Content backend\.env
```

Debe tener:
```
SQLALCHEMY_DATABASE_URI=postgresql://postgres@localhost:5432/limpieza_empresas
```

### Error: CORS en Frontend

Verificar que `backend/.env` tenga:
```
CORS_ORIGINS=http://localhost:3001,http://localhost:3000
```

Reiniciar backend (Ctrl+C y `python run.py`)

### Error: Puerto ocupado

```powershell
# Ver qué usa el puerto
netstat -ano | findstr :5001
netstat -ano | findstr :3001

# Matar proceso
taskkill /PID <PID> /F
```

---

## 🔄 Detener Todo

### Detener Backend:
En la terminal del backend: `Ctrl + C`

### Detener Frontend:
En la terminal del frontend: `Ctrl + C`

---

## 📊 Resumen de URLs

| Servicio | URL |
|----------|-----|
| Frontend | http://localhost:3001 |
| Backend API | http://localhost:5001 |
| PostgreSQL | localhost:5432 |

---

## 🎯 Checklist de Setup

- [ ] PostgreSQL instalado y corriendo
- [ ] Base de datos `limpieza_empresas` creada
- [ ] Tablas creadas con `schema.sql`
- [ ] Backend: venv creado
- [ ] Backend: archivo `.env` creado
- [ ] Backend: dependencias instaladas
- [ ] Backend: datos de ejemplo cargados
- [ ] Frontend: archivo `.env` creado
- [ ] Frontend: dependencias npm instaladas
- [ ] Backend corriendo en terminal 1
- [ ] Frontend corriendo en terminal 2
- [ ] Aplicación cargando en navegador
- [ ] 5 módulos funcionando (Empresas, Servicios, Contratos, Permisos, Empleados)

---

## 🎉 ¡Todo Listo!

Tu aplicación está corriendo localmente con:
- ✅ PostgreSQL
- ✅ Backend Flask
- ✅ Frontend React
- ✅ 5 módulos CRUD completos

**¡Disfruta de tu aplicación!** 🚀

