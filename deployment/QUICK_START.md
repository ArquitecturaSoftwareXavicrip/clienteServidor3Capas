# Guía Rápida de Despliegue en 3 Nodos

## Resumen de Pasos

### Preparación Previa
1. Asegúrate de que los 3 nodos están en la misma red local
2. Anota las IPs de cada nodo
3. Acceso SSH a cada nodo con permisos sudo

### Node 1: Database (192.168.1.10)

```bash
# Conectarse al nodo
ssh usuario@192.168.1.10

# Ejecutar script de setup
bash node1-database-setup.sh

# Verificar
sudo systemctl status postgresql
psql -h localhost -U limpieza_user -d limpieza_empresas
```

### Node 2: Backend (192.168.1.20)

```bash
# Conectarse al nodo
ssh usuario@192.168.1.20

# Ejecutar script de setup
bash node2-backend-setup.sh

# Verificar
sudo systemctl status limpieza-backend
curl http://192.168.1.20:5001/
```

### Node 3: Frontend (192.168.1.30)

```bash
# Conectarse al nodo
ssh usuario@192.168.1.30

# Ejecutar script de setup
bash node3-frontend-setup.sh

# Verificar
sudo systemctl status nginx
curl http://192.168.1.30:3001/
```

## Verificación de Conectividad

### Desde Node 2 - Conectar a Database
```bash
psql -h 192.168.1.10 -U limpieza_user -d limpieza_empresas -c "SELECT version();"
```

### Desde Node 3 - Conectar a Backend
```bash
curl http://192.168.1.20:5001/api/empresas
```

### Desde tu máquina local
```bash
# Verificar Database (debería fallar - no responde HTTP)
curl http://192.168.1.10:5432

# Verificar Backend
curl http://192.168.1.20:5001/

# Verificar Frontend
curl http://192.168.1.30:3001/
```

## Prueba Completa del Flujo

1. **Abrir navegador**: http://192.168.1.30:3001
2. **Crear una empresa** desde el frontend
3. **Verificar en la base de datos**:
   ```bash
   psql -h 192.168.1.10 -U limpieza_user -d limpieza_empresas
   SELECT * FROM empresas;
   ```
4. **Verificar logs del backend**:
   ```bash
   sudo journalctl -u limpieza-backend -f
   ```

## Configuración de IPs Personalizadas

Si tus IPs son diferentes a las del ejemplo, edita los archivos:

1. **Backend .env** (`/opt/limpieza/arqCS-NCapas/backend/.env`):
   ```env
   SQLALCHEMY_DATABASE_URI=postgresql://limpieza_user:contraseña_segura_123@TU_IP_NODE1:5432/limpieza_empresas
   CORS_ORIGINS=http://TU_IP_NODE3:3001
   ```

2. **Frontend .env** (`/opt/limpieza/arqCS-NCapas/frontend/.env`):
   ```env
   REACT_APP_API_URL=http://TU_IP_NODE2:5001/api
   ```

3. **Nginx config** (Node 3):
   ```bash
   sudo nano /etc/nginx/sites-available/limpieza-frontend
   # Cambiar: server_name TU_IP_NODE3;
   ```

Luego reinicia los servicios:
```bash
# Node 2
sudo systemctl restart limpieza-backend

# Node 3
npm run build
sudo systemctl restart nginx
```

## Monitoreo Continuo

### Ver logs en tiempo real

**Node 1 (Database)**:
```bash
sudo journalctl -u postgresql -f
```

**Node 2 (Backend)**:
```bash
sudo journalctl -u limpieza-backend -f
```

**Node 3 (Frontend)**:
```bash
sudo tail -f /var/log/nginx/access.log
sudo tail -f /var/log/nginx/error.log
```

## Detener/Reiniciar Servicios

```bash
# Node 1
sudo systemctl stop postgresql
sudo systemctl start postgresql

# Node 2
sudo systemctl stop limpieza-backend
sudo systemctl start limpieza-backend

# Node 3
sudo systemctl stop nginx
sudo systemctl start nginx
```

## Troubleshooting Rápido

| Problema | Solución |
|----------|----------|
| Backend no conecta a DB | Verificar firewall en Node 1: `sudo ufw status` |
| Frontend no ve Backend | Verificar CORS_ORIGINS en .env del backend |
| Nginx no sirve frontend | Verificar que `npm run build` se ejecutó |
| Servicios no inician | Verificar logs: `sudo journalctl -u [servicio] -n 50` |
| Puertos en uso | `sudo netstat -tulpn \| grep [puerto]` |
