# Configuración PostgreSQL para Backend

## 📋 Configuración de Variables de Entorno

Crea un archivo `.env` en la carpeta `backend/` con el siguiente contenido:

### Opción 1: PostgreSQL SIN contraseña (tu caso)

```env
FLASK_ENV=development
PORT=5001
SECRET_KEY=dev-secret-key-change-in-production

# PostgreSQL sin contraseña
SQLALCHEMY_DATABASE_URI=postgresql://postgres@localhost:5432/limpieza_empresas

# CORS
CORS_ORIGINS=http://localhost:3001,http://localhost:3000
```

### Opción 2: PostgreSQL CON contraseña

```env
FLASK_ENV=development
PORT=5001
SECRET_KEY=dev-secret-key-change-in-production

# PostgreSQL con contraseña
SQLALCHEMY_DATABASE_URI=postgresql://postgres:tu_contraseña@localhost:5432/limpieza_empresas

# CORS
CORS_ORIGINS=http://localhost:3001,http://localhost:3000
```

### Opción 3: Despliegue en 3 Nodos

```env
FLASK_ENV=production
PORT=5001
SECRET_KEY=clave-super-secreta-generada-aleatoriamente

# PostgreSQL en Nodo 1 (sin contraseña)
SQLALCHEMY_DATABASE_URI=postgresql://postgres@192.168.1.10:5432/limpieza_empresas

# CORS (IP del Nodo 3 - Frontend)
CORS_ORIGINS=http://192.168.1.30:3001
```

## 🔧 Pasos para Configurar PostgreSQL

### 1. Instalar PostgreSQL

**Windows:**
- Descargar desde: https://www.postgresql.org/download/windows/
- O usar: `winget install PostgreSQL.PostgreSQL`

**Linux:**
```bash
sudo apt update
sudo apt install postgresql postgresql-contrib
```

### 2. Crear Base de Datos

```bash
# Conectar a PostgreSQL (sin contraseña)
psql -U postgres

# Dentro de psql:
CREATE DATABASE limpieza_empresas;

# Verificar
\l

# Salir
\q
```

### 3. Instalar Dependencias Python

```bash
cd backend
pip install psycopg2-binary python-dotenv
```

### 4. Crear Archivo .env

```bash
# Windows PowerShell
cd backend
New-Item -Path .env -ItemType File
notepad .env

# Linux/Mac
cd backend
nano .env
```

Pega el contenido de la Opción 1 (sin contraseña).

### 5. Verificar Configuración

```bash
# Activar entorno virtual
python -m venv venv
.\venv\Scripts\Activate.ps1  # Windows
# source venv/bin/activate    # Linux/Mac

# Instalar dependencias
pip install -r requirements.txt

# Verificar conexión a PostgreSQL
python -c "from app import create_app; app = create_app(); print('Conexión exitosa!')"
```

### 6. Inicializar Base de Datos

```bash
# Crear tablas
cd ../database
python init_db.py

# Cargar datos de permisos
python init_permisos.py
```

## 🐛 Troubleshooting

### Error: "could not connect to server"

PostgreSQL no está corriendo:

```bash
# Windows
# Ir a Servicios y iniciar "postgresql-x64-XX"

# Linux
sudo systemctl start postgresql
sudo systemctl enable postgresql
```

### Error: "FATAL: password authentication failed"

Tu PostgreSQL requiere contraseña. Opciones:

**Opción A:** Usar contraseña en .env
```env
SQLALCHEMY_DATABASE_URI=postgresql://postgres:tu_contraseña@localhost:5432/limpieza_empresas
```

**Opción B:** Configurar trust authentication (sin contraseña)

En Windows: `C:\Program Files\PostgreSQL\XX\data\pg_hba.conf`  
En Linux: `/etc/postgresql/XX/main/pg_hba.conf`

Cambiar:
```
# IPv4 local connections:
host    all             all             127.0.0.1/32            md5
```

Por:
```
# IPv4 local connections:
host    all             all             127.0.0.1/32            trust
```

Reiniciar PostgreSQL:
```bash
# Windows
net stop postgresql-x64-XX
net start postgresql-x64-XX

# Linux
sudo systemctl restart postgresql
```

### Error: "database 'limpieza_empresas' does not exist"

```bash
psql -U postgres -c "CREATE DATABASE limpieza_empresas;"
```

### Error: "psycopg2" not installed

```bash
pip install psycopg2-binary
```

## 📝 Formato del URI de Conexión

```
postgresql://[usuario]:[contraseña]@[host]:[puerto]/[base_de_datos]
```

Ejemplos:
- `postgresql://postgres@localhost:5432/limpieza_empresas` (sin contraseña)
- `postgresql://postgres:password@localhost:5432/limpieza_empresas` (con contraseña)
- `postgresql://user:pass@192.168.1.10:5432/dbname` (remoto)

## 🚀 Quick Start (Sin Contraseña)

```bash
# 1. Crear base de datos
psql -U postgres -c "CREATE DATABASE limpieza_empresas;"

# 2. Crear archivo .env
cd backend
echo 'FLASK_ENV=development' > .env
echo 'PORT=5001' >> .env
echo 'SECRET_KEY=dev-key' >> .env
echo 'SQLALCHEMY_DATABASE_URI=postgresql://postgres@localhost:5432/limpieza_empresas' >> .env
echo 'CORS_ORIGINS=http://localhost:3001' >> .env

# 3. Instalar dependencias
pip install -r requirements.txt

# 4. Inicializar base de datos
cd ../database
python init_db.py
python init_permisos.py

# 5. Ejecutar backend
cd ../backend
python run.py
```

¡Listo! Backend corriendo con PostgreSQL en http://localhost:5001

