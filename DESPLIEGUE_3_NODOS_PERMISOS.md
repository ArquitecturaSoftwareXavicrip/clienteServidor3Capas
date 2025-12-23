# 🚀 Guía de Despliegue en 3 Nodos - Incluye Módulo de Permisos

## 📋 Resumen

Esta guía te enseña cómo desplegar la aplicación completa (incluyendo el módulo de Permisos) en **3 nodos físicos diferentes** usando **PostgreSQL SIN contraseña**.

---

## 🏗️ Arquitectura

```
┌──────────────────────────────────────────────────────────┐
│                    RED LOCAL                             │
│                                                          │
│  ┌─────────────────┐    ┌──────────────────┐          │
│  │   NODO 1        │    │   NODO 2         │          │
│  │   PostgreSQL    │◄───┤   Flask Backend  │          │
│  │   192.168.1.10  │    │   192.168.1.20   │          │
│  │   Puerto: 5432  │    │   Puerto: 5001   │          │
│  └─────────────────┘    └────────┬─────────┘          │
│                                   │                     │
│                                   │ HTTP/REST           │
│                                   ▼                     │
│                          ┌──────────────────┐          │
│                          │   NODO 3         │          │
│                          │   React Frontend │          │
│                          │   192.168.1.30   │          │
│                          │   Puerto: 3001   │          │
│                          └──────────────────┘          │
└──────────────────────────────────────────────────────────┘
```

---

## 🎯 Nodo 1: Base de Datos (PostgreSQL)

### Paso 1: Instalar PostgreSQL

```bash
# Conectarse al Nodo 1
ssh usuario@192.168.1.10

# Actualizar sistema
sudo apt update && sudo apt upgrade -y

# Instalar PostgreSQL
sudo apt install postgresql postgresql-contrib -y

# Verificar instalación
sudo systemctl status postgresql
```

### Paso 2: Crear Base de Datos

```bash
# Conectarse como postgres
sudo -u postgres psql

# Crear base de datos
CREATE DATABASE limpieza_empresas;

# Verificar
\l

# Salir
\q
```

### Paso 3: Configurar Acceso Remoto SIN Contraseña

```bash
# Editar postgresql.conf
sudo nano /etc/postgresql/15/main/postgresql.conf

# Buscar y modificar:
listen_addresses = '*'  # En lugar de 'localhost'
```

```bash
# Configurar pg_hba.conf para acceso SIN contraseña
sudo nano /etc/postgresql/15/main/pg_hba.conf

# Agregar al final:
host    limpieza_empresas    postgres    192.168.1.0/24    trust
```

### Paso 4: Crear Tablas

```bash
# Conectarse a la base de datos
sudo -u postgres psql limpieza_empresas

# Copiar y pegar el contenido de database/schema.sql:
```

```sql
-- Tabla de Empresas
CREATE TABLE IF NOT EXISTS empresas (
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    direccion VARCHAR(200) NOT NULL,
    telefono VARCHAR(20) NOT NULL,
    email VARCHAR(100) NOT NULL
);

-- Tabla de Servicios
CREATE TABLE IF NOT EXISTS servicios (
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    descripcion TEXT,
    precio_base REAL NOT NULL,
    duracion_horas REAL NOT NULL
);

-- Tabla de Contratos
CREATE TABLE IF NOT EXISTS contratos (
    id SERIAL PRIMARY KEY,
    empresa_id INTEGER NOT NULL,
    servicio_id INTEGER NOT NULL,
    fecha_inicio DATE NOT NULL,
    fecha_fin DATE,
    estado VARCHAR(20) NOT NULL DEFAULT 'activo',
    precio_final REAL NOT NULL,
    FOREIGN KEY (empresa_id) REFERENCES empresas(id) ON DELETE CASCADE,
    FOREIGN KEY (servicio_id) REFERENCES servicios(id) ON DELETE CASCADE
);

-- Tabla de Permisos (Vacaciones)
CREATE TABLE IF NOT EXISTS permisos (
    id SERIAL PRIMARY KEY,
    empleado VARCHAR(100) NOT NULL,
    tipo VARCHAR(50) NOT NULL DEFAULT 'Vacaciones',
    fecha_inicio DATE NOT NULL,
    fecha_fin DATE NOT NULL,
    dias_solicitados INTEGER NOT NULL,
    estado VARCHAR(20) NOT NULL DEFAULT 'pendiente',
    observaciones TEXT
);

-- Índices para mejorar rendimiento
CREATE INDEX IF NOT EXISTS idx_contratos_empresa ON contratos(empresa_id);
CREATE INDEX IF NOT EXISTS idx_contratos_servicio ON contratos(servicio_id);
CREATE INDEX IF NOT EXISTS idx_permisos_estado ON permisos(estado);
CREATE INDEX IF NOT EXISTS idx_permisos_empleado ON permisos(empleado);
```

```bash
# Salir
\q
```

### Paso 5: Reiniciar PostgreSQL

```bash
sudo systemctl restart postgresql
sudo systemctl enable postgresql

# Verificar que está escuchando
sudo netstat -tulpn | grep 5432
```

### Paso 6: Configurar Firewall

```bash
# Permitir conexiones desde la red local
sudo ufw allow from 192.168.1.0/24 to any port 5432
sudo ufw enable
sudo ufw status
```

### Paso 7: Verificar Conexión Remota

```bash
# Desde el Nodo 2, probar:
psql -h 192.168.1.10 -U postgres -d limpieza_empresas -c "SELECT version();"

# Debería mostrar la versión de PostgreSQL
```

---

## 🐍 Nodo 2: Backend (Flask API)

### Paso 1: Preparar Entorno

```bash
# Conectarse al Nodo 2
ssh usuario@192.168.1.20

# Actualizar sistema
sudo apt update && sudo apt upgrade -y

# Instalar Python y herramientas
sudo apt install python3 python3-pip python3-venv git postgresql-client -y
```

### Paso 2: Clonar Repositorio

```bash
# Crear directorio
mkdir -p /opt/limpieza
cd /opt/limpieza

# Clonar (o copiar con scp)
git clone <tu-repositorio>
cd clienteServidor3Capas/backend
```

### Paso 3: Configurar Entorno Virtual

```bash
# Crear entorno virtual
python3 -m venv venv

# Activar
source venv/bin/activate

# Instalar dependencias
pip install --upgrade pip
pip install -r requirements.txt
pip install psycopg2-binary
```

### Paso 4: Crear Archivo .env

```bash
nano .env
```

**Contenido del archivo `.env`**:

```env
FLASK_ENV=production
PORT=5001
SECRET_KEY=tu-clave-secreta-super-segura-cambiar-en-produccion

# PostgreSQL SIN contraseña en Nodo 1
SQLALCHEMY_DATABASE_URI=postgresql://postgres@192.168.1.10:5432/limpieza_empresas

# CORS (IP del Nodo 3 - Frontend)
CORS_ORIGINS=http://192.168.1.30:3001,http://localhost:3001
```

### Paso 5: Verificar Conexión a Base de Datos

```bash
# Verificar que puedes conectarte
psql -h 192.168.1.10 -U postgres -d limpieza_empresas -c "SELECT count(*) FROM empresas;"

# Debería devolver 0 (tabla vacía)
```

### Paso 6: Inicializar Datos

```bash
# Activar entorno virtual
source venv/bin/activate

# Cargar datos de ejemplo
cd ../database
python3 init_db.py
python3 init_permisos.py

# Volver a backend
cd ../backend
```

### Paso 7: Configurar como Servicio

```bash
# Crear archivo de servicio
sudo nano /etc/systemd/system/limpieza-backend.service
```

**Contenido**:

```ini
[Unit]
Description=Limpieza Backend Service (Tier 2)
After=network.target

[Service]
Type=simple
User=www-data
WorkingDirectory=/opt/limpieza/clienteServidor3Capas/backend
Environment="PATH=/opt/limpieza/clienteServidor3Capas/backend/venv/bin"
EnvironmentFile=/opt/limpieza/clienteServidor3Capas/backend/.env
ExecStart=/opt/limpieza/clienteServidor3Capas/backend/venv/bin/python run.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

```bash
# Recargar systemd
sudo systemctl daemon-reload

# Habilitar e iniciar
sudo systemctl enable limpieza-backend
sudo systemctl start limpieza-backend

# Verificar estado
sudo systemctl status limpieza-backend

# Ver logs
sudo journalctl -u limpieza-backend -f
```

### Paso 8: Configurar Firewall

```bash
# Permitir puerto 5001 desde la red local
sudo ufw allow from 192.168.1.0/24 to any port 5001
sudo ufw enable
sudo ufw status
```

### Paso 9: Verificar Funcionamiento

```bash
# Probar API
curl http://192.168.1.20:5001/

# Debería devolver:
# {"message": "API de Servicios de Limpieza para Empresas", "version": "1.0"}

# Probar endpoints
curl http://192.168.1.20:5001/api/empresas
curl http://192.168.1.20:5001/api/servicios
curl http://192.168.1.20:5001/api/contratos
curl http://192.168.1.20:5001/api/permisos
```

---

## ⚛️ Nodo 3: Frontend (React)

### Paso 1: Preparar Entorno

```bash
# Conectarse al Nodo 3
ssh usuario@192.168.1.30

# Actualizar sistema
sudo apt update && sudo apt upgrade -y

# Instalar Node.js 18
curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash -
sudo apt install -y nodejs git
```

### Paso 2: Clonar Repositorio

```bash
# Crear directorio
mkdir -p /opt/limpieza
cd /opt/limpieza

# Clonar (o copiar con scp)
git clone <tu-repositorio>
cd clienteServidor3Capas/frontend
```

### Paso 3: Instalar Dependencias

```bash
# Instalar dependencias
npm install
```

### Paso 4: Configurar Variables de Entorno

```bash
nano .env
```

**Contenido**:

```env
REACT_APP_API_URL=http://192.168.1.20:5001/api
PORT=3001
```

### Paso 5: Construir para Producción

```bash
# Construir aplicación
npm run build

# Verificar que se creó build/
ls -la build/
```

### Paso 6: Instalar y Configurar Nginx

```bash
# Instalar Nginx
sudo apt install nginx -y

# Crear configuración
sudo nano /etc/nginx/sites-available/limpieza-frontend
```

**Contenido de Nginx**:

```nginx
server {
    listen 3001;
    server_name 192.168.1.30;

    root /opt/limpieza/clienteServidor3Capas/frontend/build;
    index index.html;

    # React Router
    location / {
        try_files $uri $uri/ /index.html;
    }

    # Archivos estáticos
    location /static {
        alias /opt/limpieza/clienteServidor3Capas/frontend/build/static;
        expires 1y;
        add_header Cache-Control "public, immutable";
    }

    # Headers de seguridad
    add_header X-Frame-Options "SAMEORIGIN" always;
    add_header X-Content-Type-Options "nosniff" always;
    add_header X-XSS-Protection "1; mode=block" always;
}
```

```bash
# Habilitar sitio
sudo ln -s /etc/nginx/sites-available/limpieza-frontend /etc/nginx/sites-enabled/

# Verificar configuración
sudo nginx -t

# Reiniciar Nginx
sudo systemctl restart nginx
sudo systemctl enable nginx

# Verificar estado
sudo systemctl status nginx
```

### Paso 7: Configurar Firewall

```bash
# Permitir puerto 3001
sudo ufw allow from 192.168.1.0/24 to any port 3001
sudo ufw allow 'Nginx Full'
sudo ufw enable
sudo ufw status
```

### Paso 8: Verificar Funcionamiento

```bash
# Probar con curl
curl http://192.168.1.30:3001/

# Debería devolver HTML de React
```

---

## ✅ Verificación Final

### 1. Probar Conectividad entre Nodos

```bash
# Desde Nodo 2, conectar a Nodo 1
psql -h 192.168.1.10 -U postgres -d limpieza_empresas -c "SELECT count(*) FROM permisos;"

# Desde Nodo 3, conectar a Nodo 2
curl http://192.168.1.20:5001/api/permisos
```

### 2. Probar Aplicación Completa

1. Abrir navegador en `http://192.168.1.30:3001`
2. Ver que carga la aplicación
3. Hacer clic en "Permisos"
4. Ver los permisos de ejemplo
5. Crear un nuevo permiso
6. Aprobar un permiso pendiente
7. Verificar en la base de datos:

```bash
psql -h 192.168.1.10 -U postgres -d limpieza_empresas
SELECT * FROM permisos;
\q
```

### 3. Verificar Logs

```bash
# Nodo 1 (Database)
sudo journalctl -u postgresql -n 50

# Nodo 2 (Backend)
sudo journalctl -u limpieza-backend -f

# Nodo 3 (Frontend)
sudo tail -f /var/log/nginx/access.log
```

---

## 📊 Checklist de Despliegue

### Nodo 1 (Database)
- [ ] PostgreSQL instalado y corriendo
- [ ] Base de datos `limpieza_empresas` creada
- [ ] Tablas creadas (empresas, servicios, contratos, permisos)
- [ ] Acceso remoto configurado (trust)
- [ ] Firewall configurado (puerto 5432)
- [ ] Conexión remota probada

### Nodo 2 (Backend)
- [ ] Python 3 y dependencias instaladas
- [ ] Código clonado/copiado
- [ ] Entorno virtual creado
- [ ] Archivo .env configurado
- [ ] Conexión a PostgreSQL verificada
- [ ] Datos de ejemplo cargados
- [ ] Servicio systemd configurado
- [ ] Backend accesible desde red local
- [ ] Firewall configurado (puerto 5001)
- [ ] Logs funcionando

### Nodo 3 (Frontend)
- [ ] Node.js instalado
- [ ] Código clonado/copiado
- [ ] Dependencias npm instaladas
- [ ] Archivo .env configurado
- [ ] Build de producción creado
- [ ] Nginx instalado y configurado
- [ ] Frontend accesible desde navegador
- [ ] Firewall configurado (puerto 3001)
- [ ] Conexión al backend verificada

### Verificación Final
- [ ] Flujo completo probado (crear permiso, aprobar, ver en BD)
- [ ] Módulo de Permisos funcional
- [ ] Módulo de Empresas funcional
- [ ] Módulo de Servicios funcional
- [ ] Módulo de Contratos funcional
- [ ] Todos los servicios inician automáticamente

---

## 🐛 Solución de Problemas

### Error: Backend no puede conectar a PostgreSQL

```bash
# Verificar que PostgreSQL está corriendo en Nodo 1
ssh usuario@192.168.1.10
sudo systemctl status postgresql

# Verificar que puede conectarse desde Nodo 2
ssh usuario@192.168.1.20
psql -h 192.168.1.10 -U postgres -d limpieza_empresas

# Verificar pg_hba.conf
sudo cat /etc/postgresql/15/main/pg_hba.conf | grep trust
```

### Error: CORS en Frontend

```bash
# Verificar CORS_ORIGINS en Nodo 2
cat /opt/limpieza/clienteServidor3Capas/backend/.env | grep CORS

# Reiniciar backend
sudo systemctl restart limpieza-backend
```

### Error: Frontend muestra página en blanco

```bash
# Verificar build
ls -la /opt/limpieza/clienteServidor3Capas/frontend/build/

# Verificar Nginx
sudo nginx -t
sudo systemctl restart nginx

# Ver logs
sudo tail -f /var/log/nginx/error.log
```

---

## 🎉 ¡Listo!

Tu aplicación está corriendo en 3 nodos con PostgreSQL y el módulo de Permisos funcionando.

**URLs:**
- Frontend: http://192.168.1.30:3001
- Backend API: http://192.168.1.20:5001
- PostgreSQL: 192.168.1.10:5432

**Próximos pasos:**
- Configurar backups automáticos
- Implementar SSL/TLS
- Configurar monitoreo
- Agregar balanceador de carga

