# 🚀 Migración a PostgreSQL y Despliegue en 3 Nodos

## 📋 Resumen

Este documento explica cómo migrar el proyecto de SQLite a **PostgreSQL SIN contraseña** y desplegarlo en **3 nodos físicos diferentes**.

---

## 🎯 Cambios Realizados

### ✅ Base de Datos
- ✅ `database/schema.sql` actualizado para PostgreSQL (SERIAL en lugar de AUTOINCREMENT)
- ✅ Agregada tabla `permisos` con índices para mejorar rendimiento
- ✅ `init_db.py` compatible con PostgreSQL vía SQLAlchemy
- ✅ `init_permisos.py` compatible con PostgreSQL

### ✅ Backend
- ✅ `backend/CONFIG_POSTGRESQL.md` - Guía de configuración completa
- ✅ Backend ya usa SQLAlchemy ORM (compatible con PostgreSQL)
- ✅ Solo necesita cambiar `SQLALCHEMY_DATABASE_URI` en `.env`

### ✅ Documentación
- ✅ `DESPLIEGUE_3_NODOS_PERMISOS.md` - Guía paso a paso completa
- ✅ `MIGRACION_POSTGRESQL_3_NODOS.md` - Este documento

### ✅ Scripts de Automatización
- ✅ `database/setup_postgresql.sh` - Setup automático de PostgreSQL
- ✅ `backend/setup_backend.sh` - Setup automático de Backend
- ✅ `frontend/setup_frontend.sh` - Setup automático de Frontend

---

## 🚀 Inicio Rápido

### Opción 1: Despliegue Local (1 máquina con PostgreSQL)

```bash
# 1. Instalar PostgreSQL
sudo apt install postgresql postgresql-contrib

# 2. Crear base de datos
sudo -u postgres psql -c "CREATE DATABASE limpieza_empresas;"

# 3. Crear tablas
cd database
sudo -u postgres psql limpieza_empresas -f schema.sql

# 4. Configurar Backend
cd ../backend
cat > .env << EOF
FLASK_ENV=development
PORT=5001
SECRET_KEY=dev-key
SQLALCHEMY_DATABASE_URI=postgresql://postgres@localhost:5432/limpieza_empresas
CORS_ORIGINS=http://localhost:3001
EOF

# 5. Instalar dependencias y cargar datos
python3 -m venv venv
source venv/bin/activate  # Windows: .\venv\Scripts\Activate.ps1
pip install -r requirements.txt
pip install psycopg2-binary
cd ../database
python3 init_db.py
python3 init_permisos.py

# 6. Ejecutar Backend
cd ../backend
python run.py

# 7. En otra terminal, ejecutar Frontend
cd frontend
npm install
npm start

# Abrir http://localhost:3001
```

### Opción 2: Despliegue en 3 Nodos (recomendado)

Sigue la guía completa: **`DESPLIEGUE_3_NODOS_PERMISOS.md`**

O usa los scripts automáticos:

```bash
# NODO 1 (Base de Datos)
cd database
chmod +x setup_postgresql.sh
./setup_postgresql.sh

# NODO 2 (Backend)
cd backend
chmod +x setup_backend.sh
./setup_backend.sh

# NODO 3 (Frontend)
cd frontend
chmod +x setup_frontend.sh
./setup_frontend.sh
```

---

## 🔧 Configuración PostgreSQL SIN Contraseña

### Método 1: Trust Authentication (Recomendado para desarrollo)

Editar `/etc/postgresql/15/main/pg_hba.conf`:

```conf
# IPv4 local connections:
host    all             all             127.0.0.1/32            trust

# Para red local (3 nodos):
host    limpieza_empresas    postgres    192.168.1.0/24    trust
```

Reiniciar PostgreSQL:
```bash
sudo systemctl restart postgresql
```

### Método 2: Usuario postgres sin contraseña

```bash
sudo -u postgres psql
ALTER USER postgres WITH PASSWORD NULL;
```

### URI de Conexión

```
postgresql://postgres@localhost:5432/limpieza_empresas
```

O para 3 nodos (Backend conectándose al Nodo 1):
```
postgresql://postgres@192.168.1.10:5432/limpieza_empresas
```

---

## 📊 Arquitectura de 3 Nodos

```
┌────────────────────────────────────────────────────────────┐
│                        RED LOCAL                           │
│                                                            │
│  ┌──────────────────┐                                     │
│  │   NODO 1         │                                     │
│  │   PostgreSQL     │  Tier 3: Datos                      │
│  │   192.168.1.10   │  - Base de datos limpieza_empresas  │
│  │   Puerto: 5432   │  - Tablas: empresas, servicios,     │
│  └────────┬─────────┘    contratos, permisos              │
│           │                                                │
│           │ SQL (trust, sin contraseña)                   │
│           ▼                                                │
│  ┌──────────────────┐                                     │
│  │   NODO 2         │                                     │
│  │   Flask Backend  │  Tier 2: Lógica de Negocio         │
│  │   192.168.1.20   │  - API RESTful                      │
│  │   Puerto: 5001   │  - Controladores, Servicios,        │
│  └────────┬─────────┘    Repositorios                     │
│           │                                                │
│           │ HTTP/REST                                      │
│           ▼                                                │
│  ┌──────────────────┐                                     │
│  │   NODO 3         │                                     │
│  │   React Frontend │  Tier 1: Presentación              │
│  │   192.168.1.30   │  - Vistas React                     │
│  │   Puerto: 3001   │  - Módulos: Empresas, Servicios,    │
│  └──────────────────┘    Contratos, Permisos              │
│                                                            │
└────────────────────────────────────────────────────────────┘
```

---

## 📝 Pasos Detallados

### NODO 1: PostgreSQL (Tier 3)

#### 1. Instalar PostgreSQL

```bash
ssh usuario@192.168.1.10
sudo apt update
sudo apt install postgresql postgresql-contrib -y
```

#### 2. Crear Base de Datos

```bash
sudo -u postgres psql
CREATE DATABASE limpieza_empresas;
\q
```

#### 3. Crear Tablas

```bash
cd database
sudo -u postgres psql limpieza_empresas -f schema.sql
```

#### 4. Configurar Acceso Remoto

```bash
sudo nano /etc/postgresql/15/main/postgresql.conf
# Cambiar: listen_addresses = '*'

sudo nano /etc/postgresql/15/main/pg_hba.conf
# Agregar: host limpieza_empresas postgres 192.168.1.0/24 trust

sudo systemctl restart postgresql
```

#### 5. Configurar Firewall

```bash
sudo ufw allow from 192.168.1.0/24 to any port 5432
sudo ufw enable
```

---

### NODO 2: Backend Flask (Tier 2)

#### 1. Instalar Dependencias

```bash
ssh usuario@192.168.1.20
sudo apt update
sudo apt install python3 python3-pip python3-venv git postgresql-client -y
```

#### 2. Clonar Proyecto

```bash
mkdir -p /opt/limpieza
cd /opt/limpieza
git clone <tu-repo>
cd clienteServidor3Capas/backend
```

#### 3. Configurar Entorno

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
pip install psycopg2-binary
```

#### 4. Crear .env

```bash
cat > .env << EOF
FLASK_ENV=production
PORT=5001
SECRET_KEY=$(openssl rand -hex 32)
SQLALCHEMY_DATABASE_URI=postgresql://postgres@192.168.1.10:5432/limpieza_empresas
CORS_ORIGINS=http://192.168.1.30:3001
EOF
```

#### 5. Cargar Datos

```bash
cd ../database
python3 init_db.py
python3 init_permisos.py
```

#### 6. Crear Servicio Systemd

```bash
sudo nano /etc/systemd/system/limpieza-backend.service
```

Contenido:
```ini
[Unit]
Description=Limpieza Backend Service
After=network.target

[Service]
Type=simple
User=$USER
WorkingDirectory=/opt/limpieza/clienteServidor3Capas/backend
Environment="PATH=/opt/limpieza/clienteServidor3Capas/backend/venv/bin"
EnvironmentFile=/opt/limpieza/clienteServidor3Capas/backend/.env
ExecStart=/opt/limpieza/clienteServidor3Capas/backend/venv/bin/python run.py
Restart=always

[Install]
WantedBy=multi-user.target
```

```bash
sudo systemctl daemon-reload
sudo systemctl enable limpieza-backend
sudo systemctl start limpieza-backend
```

#### 7. Configurar Firewall

```bash
sudo ufw allow from 192.168.1.0/24 to any port 5001
sudo ufw enable
```

---

### NODO 3: Frontend React (Tier 1)

#### 1. Instalar Node.js

```bash
ssh usuario@192.168.1.30
sudo apt update
curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash -
sudo apt install -y nodejs git nginx
```

#### 2. Clonar Proyecto

```bash
mkdir -p /opt/limpieza
cd /opt/limpieza
git clone <tu-repo>
cd clienteServidor3Capas/frontend
```

#### 3. Configurar y Construir

```bash
npm install

cat > .env << EOF
REACT_APP_API_URL=http://192.168.1.20:5001/api
PORT=3001
EOF

npm run build
```

#### 4. Configurar Nginx

```bash
sudo nano /etc/nginx/sites-available/limpieza-frontend
```

Contenido:
```nginx
server {
    listen 3001;
    server_name _;
    root /opt/limpieza/clienteServidor3Capas/frontend/build;
    index index.html;

    location / {
        try_files $uri $uri/ /index.html;
    }

    location /static {
        alias /opt/limpieza/clienteServidor3Capas/frontend/build/static;
        expires 1y;
        add_header Cache-Control "public, immutable";
    }
}
```

```bash
sudo ln -s /etc/nginx/sites-available/limpieza-frontend /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
sudo systemctl enable nginx
```

#### 5. Configurar Firewall

```bash
sudo ufw allow from 192.168.1.0/24 to any port 3001
sudo ufw allow 'Nginx Full'
sudo ufw enable
```

---

## ✅ Verificación

### 1. Verificar PostgreSQL (Nodo 1)

```bash
ssh usuario@192.168.1.10
sudo -u postgres psql limpieza_empresas -c "SELECT count(*) FROM permisos;"
```

### 2. Verificar Backend (Nodo 2)

```bash
ssh usuario@192.168.1.20
curl http://localhost:5001/
curl http://localhost:5001/api/permisos
sudo systemctl status limpieza-backend
```

### 3. Verificar Frontend (Nodo 3)

```bash
ssh usuario@192.168.1.30
curl http://localhost:3001/
sudo systemctl status nginx
```

### 4. Prueba Completa

1. Abrir navegador: `http://192.168.1.30:3001`
2. Navegar a "Permisos"
3. Crear un nuevo permiso
4. Verificar en la base de datos:
   ```bash
   psql -h 192.168.1.10 -U postgres -d limpieza_empresas
   SELECT * FROM permisos ORDER BY id DESC LIMIT 1;
   \q
   ```

---

## 🐛 Troubleshooting

### Error: Backend no conecta a PostgreSQL

```bash
# Verificar PostgreSQL corriendo
ssh usuario@192.168.1.10
sudo systemctl status postgresql

# Probar conexión desde Nodo 2
ssh usuario@192.168.1.20
psql -h 192.168.1.10 -U postgres -d limpieza_empresas

# Verificar pg_hba.conf
sudo cat /etc/postgresql/15/main/pg_hba.conf | grep trust
```

### Error: Frontend no conecta a Backend

```bash
# Verificar backend corriendo
ssh usuario@192.168.1.20
sudo systemctl status limpieza-backend
curl http://localhost:5001/

# Verificar CORS
cat /opt/limpieza/clienteServidor3Capas/backend/.env | grep CORS
```

### Error: "could not connect to server"

PostgreSQL no está corriendo:
```bash
sudo systemctl start postgresql
```

### Error: "FATAL: database does not exist"

```bash
sudo -u postgres psql -c "CREATE DATABASE limpieza_empresas;"
```

---

## 📚 Documentos Relacionados

1. **`DESPLIEGUE_3_NODOS_PERMISOS.md`** - Guía detallada paso a paso
2. **`backend/CONFIG_POSTGRESQL.md`** - Configuración de PostgreSQL
3. **`00_LEEME_PRIMERO.md`** - Introducción al módulo de permisos
4. **`MODULO_PERMISOS.md`** - Documentación técnica completa

---

## 🎉 ¡Listo!

Tu aplicación está corriendo en 3 nodos con PostgreSQL y el módulo de Permisos.

**URLs de Acceso:**
- Frontend: `http://192.168.1.30:3001`
- Backend API: `http://192.168.1.20:5001`
- PostgreSQL: `192.168.1.10:5432`

**Comandos Útiles:**

```bash
# Ver logs
sudo journalctl -u postgresql -f          # Nodo 1
sudo journalctl -u limpieza-backend -f    # Nodo 2
sudo tail -f /var/log/nginx/access.log    # Nodo 3

# Reiniciar servicios
sudo systemctl restart postgresql         # Nodo 1
sudo systemctl restart limpieza-backend   # Nodo 2
sudo systemctl restart nginx              # Nodo 3

# Verificar estado
sudo systemctl status postgresql          # Nodo 1
sudo systemctl status limpieza-backend    # Nodo 2
sudo systemctl status nginx               # Nodo 3
```

---

**¡Felicitaciones por completar el despliegue en 3 nodos!** 🚀

