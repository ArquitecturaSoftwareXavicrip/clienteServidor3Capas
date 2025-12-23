# Checklist de Despliegue en 3 Nodos

## Configuración de Red
- [ ] Todos los nodos están en la misma red local
- [ ] IPs configuradas correctamente:
  - Node 1 (Database): 192.168.1.10
  - Node 2 (Backend): 192.168.1.20
  - Node 3 (Frontend): 192.168.1.30
- [ ] Conectividad entre nodos verificada (ping)

## Node 1 (Database - Tier 3)
- [ ] PostgreSQL instalado y corriendo
- [ ] Base de datos `limpieza_empresas` creada
- [ ] Usuario `limpieza_user` creado con contraseña
- [ ] Acceso remoto configurado (listen_addresses = '*')
- [ ] pg_hba.conf configurado para conexiones remotas
- [ ] Firewall permite puerto 5432 desde 192.168.1.0/24
- [ ] Esquema de tablas creado (empresas, servicios, contratos)
- [ ] Conexión remota probada desde Node 2

### Comandos de Verificación (Node 1)
```bash
sudo systemctl status postgresql
sudo netstat -tulpn | grep 5432
psql -h localhost -U limpieza_user -d limpieza_empresas
```

## Node 2 (Backend - Tier 2)
- [ ] Python 3.8+ instalado
- [ ] Repositorio clonado en /opt/limpieza/arqCS-NCapas/
- [ ] Entorno virtual creado y activado
- [ ] Dependencias instaladas (pip install -r requirements.txt)
- [ ] Archivo .env configurado con:
  - SQLALCHEMY_DATABASE_URI=postgresql://limpieza_user:contraseña_segura_123@192.168.1.10:5432/limpieza_empresas
  - PORT=5001
  - CORS_ORIGINS=http://192.168.1.30:3001
- [ ] Conexión a base de datos probada
- [ ] Base de datos inicializada (init_db.py ejecutado)
- [ ] Servicio systemd creado y habilitado
- [ ] Backend corriendo en puerto 5001
- [ ] Firewall permite puerto 5001 desde 192.168.1.0/24
- [ ] API responde en http://192.168.1.20:5001/

### Comandos de Verificación (Node 2)
```bash
sudo systemctl status limpieza-backend
curl http://192.168.1.20:5001/
sudo journalctl -u limpieza-backend -f
```

## Node 3 (Frontend - Tier 1)
- [ ] Node.js 14+ instalado
- [ ] npm instalado
- [ ] Repositorio clonado en /opt/limpieza/arqCS-NCapas/
- [ ] Dependencias instaladas (npm install)
- [ ] Archivo .env configurado con:
  - REACT_APP_API_URL=http://192.168.1.20:5001/api
  - PORT=3001
- [ ] Build de producción creado (npm run build)
- [ ] Nginx instalado y configurado
- [ ] Sitio habilitado en Nginx
- [ ] Frontend accesible en http://192.168.1.30:3001/
- [ ] Firewall permite puerto 3001 desde 192.168.1.0/24
- [ ] Nginx corriendo y habilitado

### Comandos de Verificación (Node 3)
```bash
sudo systemctl status nginx
curl http://192.168.1.30:3001/
sudo tail -f /var/log/nginx/access.log
```

## Verificación Final
- [ ] Conectividad entre nodos:
  ```bash
  # Desde Node 2
  psql -h 192.168.1.10 -U limpieza_user -d limpieza_empresas -c "SELECT version();"
  
  # Desde Node 3
  curl http://192.168.1.20:5001/api/empresas
  ```

- [ ] Flujo completo probado:
  1. Abrir navegador en http://192.168.1.30:3001
  2. Crear una empresa desde el frontend
  3. Verificar en base de datos:
     ```bash
     psql -h 192.168.1.10 -U limpieza_user -d limpieza_empresas
     SELECT * FROM empresas;
     ```
  4. Verificar logs del backend:
     ```bash
     sudo journalctl -u limpieza-backend -f
     ```

- [ ] Servicios configurados para iniciar al arrancar:
  ```bash
  sudo systemctl is-enabled postgresql
  sudo systemctl is-enabled limpieza-backend
  sudo systemctl is-enabled nginx
  ```

## Solución de Problemas Comunes

### No puedo conectar desde Node 2 a Node 1
```bash
# Verificar que PostgreSQL está escuchando
sudo netstat -tulpn | grep 5432

# Verificar configuración
sudo grep listen_addresses /etc/postgresql/*/main/postgresql.conf

# Verificar pg_hba.conf
sudo cat /etc/postgresql/*/main/pg_hba.conf | grep limpieza

# Probar conexión local primero
psql -h localhost -U limpieza_user -d limpieza_empresas
```

### CORS Error en el Frontend
```bash
# Verificar que CORS_ORIGINS incluye la IP del frontend
cat /opt/limpieza/arqCS-NCapas/backend/.env | grep CORS_ORIGINS

# Reiniciar backend
sudo systemctl restart limpieza-backend

# Ver logs
sudo journalctl -u limpieza-backend | tail -20
```

### Frontend no puede conectar al Backend
```bash
# Verificar que el backend está corriendo
curl http://192.168.1.20:5001/

# Verificar variable de entorno en frontend
cat /opt/limpieza/arqCS-NCapas/frontend/.env

# Reconstruir frontend si es necesario
cd /opt/limpieza/arqCS-NCapas/frontend
npm run build
sudo systemctl restart nginx
```

## Comandos de Referencia Rápida

### Node 1 (Database)
```bash
# Iniciar/Detener PostgreSQL
sudo systemctl start postgresql
sudo systemctl stop postgresql
sudo systemctl restart postgresql

# Ver logs
sudo journalctl -u postgresql -f

# Conectar a base de datos
sudo -u postgres psql limpieza_empresas
```

### Node 2 (Backend)
```bash
# Iniciar/Detener Backend
sudo systemctl start limpieza-backend
sudo systemctl stop limpieza-backend
sudo systemctl restart limpieza-backend

# Ver logs
sudo journalctl -u limpieza-backend -f

# Verificar estado
sudo systemctl status limpieza-backend
```

### Node 3 (Frontend)
```bash
# Reiniciar Nginx
sudo systemctl restart nginx

# Ver logs de Nginx
sudo tail -f /var/log/nginx/error.log
sudo tail -f /var/log/nginx/access.log

# Reconstruir frontend
cd /opt/limpieza/arqCS-NCapas/frontend
npm run build
sudo systemctl restart nginx
```
