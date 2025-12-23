# Guía de Solución de Problemas - Despliegue en 3 Nodos

## Problemas de Conectividad entre Nodos

### Problema: No puedo conectar desde Node 2 a Node 1 (Database)

**Síntomas**:
- Error: `could not connect to server: Connection refused`
- Backend no puede iniciar o falla al conectar a la BD

**Soluciones**:

1. **Verificar que PostgreSQL está corriendo en Node 1**:
```bash
# En Node 1
sudo systemctl status postgresql
sudo systemctl start postgresql  # Si no está corriendo
```

2. **Verificar que PostgreSQL escucha en todas las interfaces**:
```bash
# En Node 1
sudo netstat -tulpn | grep 5432
# Debería mostrar: tcp  0  0 0.0.0.0:5432  0.0.0.0:*  LISTEN
```

3. **Verificar configuración de listen_addresses**:
```bash
# En Node 1
sudo grep listen_addresses /etc/postgresql/*/main/postgresql.conf
# Debería mostrar: listen_addresses = '*'
```

4. **Verificar pg_hba.conf**:
```bash
# En Node 1
sudo cat /etc/postgresql/*/main/pg_hba.conf | grep limpieza
# Debería mostrar una línea como:
# host    limpieza_empresas    limpieza_user    192.168.1.0/24    md5
```

5. **Verificar firewall en Node 1**:
```bash
# En Node 1
sudo ufw status
# Debería permitir puerto 5432 desde 192.168.1.0/24
sudo ufw allow from 192.168.1.0/24 to any port 5432
```

6. **Probar conexión desde Node 2**:
```bash
# En Node 2
psql -h 192.168.1.10 -U limpieza_user -d limpieza_empresas -c "SELECT version();"
```

7. **Si aún no funciona, reiniciar PostgreSQL**:
```bash
# En Node 1
sudo systemctl restart postgresql
```

---

## Problemas del Backend (Node 2)

### Problema: Backend no inicia o falla inmediatamente

**Síntomas**:
- `sudo systemctl status limpieza-backend` muestra error
- Logs muestran errores de importación o configuración

**Soluciones**:

1. **Verificar que el entorno virtual está correctamente configurado**:
```bash
# En Node 2
cd /opt/limpieza/arqCS-NCapas/backend
source venv/bin/activate
python3 -c "import flask; print(flask.__version__)"
```

2. **Verificar que todas las dependencias están instaladas**:
```bash
# En Node 2
source venv/bin/activate
pip install -r requirements.txt
```

3. **Verificar archivo .env**:
```bash
# En Node 2
cat /opt/limpieza/arqCS-NCapas/backend/.env
# Debería contener:
# FLASK_ENV=production
# SQLALCHEMY_DATABASE_URI=postgresql://limpieza_user:contraseña_segura_123@192.168.1.10:5432/limpieza_empresas
# PORT=5001
# SECRET_KEY=...
# CORS_ORIGINS=http://192.168.1.30:3001
```

4. **Ver logs detallados**:
```bash
# En Node 2
sudo journalctl -u limpieza-backend -n 50
sudo journalctl -u limpieza-backend -f  # Ver en tiempo real
```

5. **Probar manualmente**:
```bash
# En Node 2
cd /opt/limpieza/arqCS-NCapas/backend
source venv/bin/activate
python3 run.py
# Debería mostrar: Running on http://0.0.0.0:5001
```

### Problema: Backend corre pero no responde a solicitudes

**Síntomas**:
- `curl http://192.168.1.20:5001/` no responde
- Timeout en las solicitudes

**Soluciones**:

1. **Verificar que el backend está escuchando en el puerto correcto**:
```bash
# En Node 2
sudo netstat -tulpn | grep 5001
# Debería mostrar: tcp  0  0 0.0.0.0:5001  0.0.0.0:*  LISTEN
```

2. **Verificar firewall**:
```bash
# En Node 2
sudo ufw status
sudo ufw allow from 192.168.1.0/24 to any port 5001
```

3. **Probar localmente primero**:
```bash
# En Node 2
curl http://localhost:5001/
```

4. **Verificar que el usuario www-data tiene permisos**:
```bash
# En Node 2
sudo chown -R www-data:www-data /opt/limpieza/arqCS-NCapas/backend
```

---

## Problemas del Frontend (Node 3)

### Problema: Nginx no sirve el frontend

**Síntomas**:
- `curl http://192.168.1.30:3001/` devuelve error 404 o 403
- Nginx muestra error en logs

**Soluciones**:

1. **Verificar que Nginx está corriendo**:
```bash
# En Node 3
sudo systemctl status nginx
sudo systemctl start nginx  # Si no está corriendo
```

2. **Verificar configuración de Nginx**:
```bash
# En Node 3
sudo nginx -t
# Debería mostrar: nginx: configuration file test is successful
```

3. **Verificar que el build existe**:
```bash
# En Node 3
ls -la /opt/limpieza/arqCS-NCapas/frontend/build/
# Debería contener: index.html, static/, etc.
```

4. **Si el build no existe, reconstruir**:
```bash
# En Node 3
cd /opt/limpieza/arqCS-NCapas/frontend
npm run build
```

5. **Verificar permisos de archivos**:
```bash
# En Node 3
sudo chown -R www-data:www-data /opt/limpieza/arqCS-NCapas/frontend/build
sudo chmod -R 755 /opt/limpieza/arqCS-NCapas/frontend/build
```

6. **Ver logs de Nginx**:
```bash
# En Node 3
sudo tail -f /var/log/nginx/error.log
sudo tail -f /var/log/nginx/access.log
```

### Problema: Frontend carga pero no puede conectar al Backend

**Síntomas**:
- Frontend carga en el navegador
- Errores CORS en la consola del navegador
- No puede crear empresas o ver datos

**Soluciones**:

1. **Verificar variable de entorno en frontend**:
```bash
# En Node 3
cat /opt/limpieza/arqCS-NCapas/frontend/.env
# Debería contener:
# REACT_APP_API_URL=http://192.168.1.20:5001/api
```

2. **Verificar que el backend está accesible**:
```bash
# En Node 3
curl http://192.168.1.20:5001/
# Debería responder con JSON
```

3. **Verificar CORS en el backend**:
```bash
# En Node 2
cat /opt/limpieza/arqCS-NCapas/backend/.env | grep CORS_ORIGINS
# Debería incluir: http://192.168.1.30:3001
```

4. **Reconstruir frontend con las variables correctas**:
```bash
# En Node 3
cd /opt/limpieza/arqCS-NCapas/frontend
npm run build
sudo systemctl restart nginx
```

5. **Limpiar caché del navegador**:
- Abrir DevTools (F12)
- Ir a Application > Cache Storage
- Eliminar todos los caches
- Recargar la página (Ctrl+Shift+R)

---

## Problemas de Base de Datos

### Problema: Base de datos no se inicializa correctamente

**Síntomas**:
- Tablas no existen
- Errores al insertar datos
- Queries devuelven "table does not exist"

**Soluciones**:

1. **Verificar que las tablas existen**:
```bash
# En Node 1
psql -h localhost -U limpieza_user -d limpieza_empresas
\dt
# Debería mostrar: empresas, servicios, contratos
```

2. **Si las tablas no existen, crearlas manualmente**:
```bash
# En Node 1
psql -h localhost -U limpieza_user -d limpieza_empresas
CREATE TABLE IF NOT EXISTS empresas (
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    direccion VARCHAR(200) NOT NULL,
    telefono VARCHAR(20) NOT NULL,
    email VARCHAR(100) NOT NULL
);

CREATE TABLE IF NOT EXISTS servicios (
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    descripcion TEXT,
    precio_base REAL NOT NULL,
    duracion_horas REAL NOT NULL
);

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
```

3. **Ejecutar init_db.py desde Node 2**:
```bash
# En Node 2
cd /opt/limpieza/arqCS-NCapas/database
source ../backend/venv/bin/activate
python3 init_db.py
```

### Problema: Usuario de base de datos no tiene permisos

**Síntomas**:
- Error: "permission denied"
- Backend no puede crear tablas

**Soluciones**:

1. **Verificar permisos del usuario**:
```bash
# En Node 1
sudo -u postgres psql
\du limpieza_user
# Debería mostrar que tiene permisos CREATEDB
```

2. **Si no tiene permisos, otorgarlos**:
```bash
# En Node 1
sudo -u postgres psql
ALTER USER limpieza_user CREATEDB;
GRANT ALL PRIVILEGES ON DATABASE limpieza_empresas TO limpieza_user;
```

---

## Problemas de Firewall

### Problema: Puertos bloqueados

**Síntomas**:
- No puedo conectar entre nodos
- Conexión rechazada o timeout

**Soluciones**:

1. **Ver estado del firewall**:
```bash
# En cualquier nodo
sudo ufw status
```

2. **Permitir puertos necesarios**:
```bash
# Node 1 (Database)
sudo ufw allow from 192.168.1.0/24 to any port 5432

# Node 2 (Backend)
sudo ufw allow from 192.168.1.0/24 to any port 5001

# Node 3 (Frontend)
sudo ufw allow from 192.168.1.0/24 to any port 3001
sudo ufw allow 'Nginx Full'
```

3. **Si el firewall está deshabilitado, habilitarlo**:
```bash
sudo ufw enable
```

---

## Problemas de Servicios Systemd

### Problema: Servicio no inicia al arrancar el sistema

**Síntomas**:
- Después de reiniciar, los servicios no están corriendo
- `sudo systemctl is-enabled [servicio]` muestra "disabled"

**Soluciones**:

1. **Habilitar servicios**:
```bash
# Node 1
sudo systemctl enable postgresql

# Node 2
sudo systemctl enable limpieza-backend

# Node 3
sudo systemctl enable nginx
```

2. **Verificar que están habilitados**:
```bash
sudo systemctl is-enabled postgresql
sudo systemctl is-enabled limpieza-backend
sudo systemctl is-enabled nginx
```

---

## Verificación Completa del Sistema

Para verificar que todo está funcionando correctamente, ejecuta estos comandos:

```bash
# Node 1 - Verificar Database
sudo systemctl status postgresql
sudo netstat -tulpn | grep 5432
psql -h localhost -U limpieza_user -d limpieza_empresas -c "SELECT COUNT(*) FROM empresas;"

# Node 2 - Verificar Backend
sudo systemctl status limpieza-backend
sudo netstat -tulpn | grep 5001
curl http://localhost:5001/

# Node 3 - Verificar Frontend
sudo systemctl status nginx
sudo netstat -tulpn | grep 3001
curl http://localhost:3001/ | head -20

# Verificar conectividad entre nodos
# Desde Node 2
psql -h 192.168.1.10 -U limpieza_user -d limpieza_empresas -c "SELECT version();"

# Desde Node 3
curl http://192.168.1.20:5001/api/empresas
```

Si todos estos comandos funcionan correctamente, tu despliegue en 3 nodos está completo y funcionando.
