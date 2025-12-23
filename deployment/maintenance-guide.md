# Guía de Mantenimiento - Despliegue en 3 Nodos

## Tareas de Mantenimiento Regular

### Diarias

```bash
# Verificar estado de servicios
sudo systemctl status postgresql
sudo systemctl status limpieza-backend
sudo systemctl status nginx

# Revisar logs de errores
sudo journalctl -u postgresql --since "1 hour ago" | grep -i error
sudo journalctl -u limpieza-backend --since "1 hour ago" | grep -i error
sudo tail -20 /var/log/nginx/error.log
```

### Semanales

```bash
# Verificar espacio en disco
df -h

# Verificar uso de memoria
free -h

# Verificar conexiones activas
netstat -an | grep ESTABLISHED | wc -l

# Limpiar logs antiguos
sudo journalctl --vacuum=30d
```

### Mensuales

```bash
# Hacer backup de la base de datos
pg_dump -h 192.168.1.10 -U limpieza_user limpieza_empresas > backup_$(date +%Y%m%d).sql

# Actualizar paquetes del sistema
sudo apt update && sudo apt upgrade -y

# Revisar logs de acceso
sudo tail -100 /var/log/nginx/access.log | awk '{print $1}' | sort | uniq -c | sort -rn
```

## Backups

### Backup Manual de Base de Datos

```bash
# En Node 2 o tu máquina local
pg_dump -h 192.168.1.10 -U limpieza_user limpieza_empresas > backup_$(date +%Y%m%d_%H%M%S).sql

# Comprimir backup
gzip backup_*.sql

# Verificar backup
gunzip -c backup_*.sql.gz | head -20
```

### Restaurar desde Backup

```bash
# En Node 1
psql -h localhost -U limpieza_user limpieza_empresas < backup_20240101_120000.sql

# O si está comprimido
gunzip -c backup_20240101_120000.sql.gz | psql -h localhost -U limpieza_user limpieza_empresas
```

### Backup Automático con Cron

```bash
# En Node 1, crear script de backup
sudo nano /opt/scripts/backup-db.sh
```

Contenido:
```bash
#!/bin/bash
BACKUP_DIR="/opt/backups"
DATE=$(date +%Y%m%d_%H%M%S)

# Crear directorio si no existe
mkdir -p $BACKUP_DIR

# Hacer backup
pg_dump -h localhost -U limpieza_user limpieza_empresas | gzip > $BACKUP_DIR/backup_$DATE.sql.gz

# Mantener solo los últimos 30 días
find $BACKUP_DIR -name "backup_*.sql.gz" -mtime +30 -delete

echo "Backup completado: $BACKUP_DIR/backup_$DATE.sql.gz"
```

Hacer ejecutable y programar con cron:
```bash
sudo chmod +x /opt/scripts/backup-db.sh

# Editar crontab
sudo crontab -e

# Agregar línea para ejecutar diariamente a las 2 AM
0 2 * * * /opt/scripts/backup-db.sh
```

## Actualizaciones

### Actualizar Dependencias del Backend

```bash
# En Node 2
cd /opt/limpieza/arqCS-NCapas/backend
source venv/bin/activate

# Ver actualizaciones disponibles
pip list --outdated

# Actualizar todas las dependencias
pip install --upgrade -r requirements.txt

# Reinstalar en el entorno virtual
pip install -r requirements.txt

# Reiniciar servicio
sudo systemctl restart limpieza-backend
```

### Actualizar Dependencias del Frontend

```bash
# En Node 3
cd /opt/limpieza/arqCS-NCapas/frontend

# Ver actualizaciones disponibles
npm outdated

# Actualizar dependencias
npm update

# Reconstruir
npm run build

# Reiniciar Nginx
sudo systemctl restart nginx
```

### Actualizar PostgreSQL

```bash
# En Node 1
sudo apt update
sudo apt upgrade postgresql postgresql-contrib -y

# Verificar versión
psql --version

# Reiniciar servicio
sudo systemctl restart postgresql
```

## Monitoreo y Alertas

### Configurar Monitoreo Básico

```bash
# Instalar herramientas de monitoreo
sudo apt install htop iotop nethogs -y

# Ver uso de recursos en tiempo real
htop

# Ver I/O de disco
sudo iotop

# Ver tráfico de red
sudo nethogs
```

### Alertas por Email

```bash
# Instalar herramientas de email
sudo apt install mailutils -y

# Crear script de alerta
sudo nano /opt/scripts/check-health.sh
```

Contenido:
```bash
#!/bin/bash
EMAIL="admin@example.com"
HOSTNAME=$(hostname)

# Verificar PostgreSQL
if ! sudo systemctl is-active --quiet postgresql; then
    echo "ALERTA: PostgreSQL no está corriendo en $HOSTNAME" | mail -s "Alerta de Servicio" $EMAIL
fi

# Verificar espacio en disco
DISK_USAGE=$(df / | awk 'NR==2 {print $5}' | sed 's/%//')
if [ $DISK_USAGE -gt 80 ]; then
    echo "ALERTA: Disco lleno al ${DISK_USAGE}% en $HOSTNAME" | mail -s "Alerta de Disco" $EMAIL
fi

# Verificar memoria
MEM_USAGE=$(free | awk 'NR==2 {print int($3/$2 * 100)}')
if [ $MEM_USAGE -gt 80 ]; then
    echo "ALERTA: Memoria al ${MEM_USAGE}% en $HOSTNAME" | mail -s "Alerta de Memoria" $EMAIL
fi
```

Programar con cron:
```bash
sudo crontab -e
# Ejecutar cada 30 minutos
*/30 * * * * /opt/scripts/check-health.sh
```

## Rotación de Logs

### Configurar logrotate

```bash
# Para Backend (Node 2)
sudo nano /etc/logrotate.d/limpieza-backend
```

Contenido:
```
/var/log/limpieza-backend.log {
    daily
    rotate 14
    compress
    delaycompress
    notifempty
    create 0640 www-data www-data
    sharedscripts
    postrotate
        systemctl reload limpieza-backend > /dev/null 2>&1 || true
    endscript
}
```

```bash
# Para Frontend (Node 3)
sudo nano /etc/logrotate.d/nginx
```

Contenido:
```
/var/log/nginx/*.log {
    daily
    rotate 14
    compress
    delaycompress
    notifempty
    create 0640 www-data www-data
    sharedscripts
    postrotate
        systemctl reload nginx > /dev/null 2>&1 || true
    endscript
}
```

## Optimización de Performance

### Optimizar PostgreSQL

```bash
# En Node 1, editar postgresql.conf
sudo nano /etc/postgresql/*/main/postgresql.conf

# Aumentar shared_buffers (25% de RAM)
shared_buffers = 2GB

# Aumentar effective_cache_size (50-75% de RAM)
effective_cache_size = 6GB

# Aumentar work_mem (RAM / max_connections / 2)
work_mem = 10MB

# Aumentar maintenance_work_mem
maintenance_work_mem = 512MB

# Reiniciar PostgreSQL
sudo systemctl restart postgresql
```

### Optimizar Flask Backend

```bash
# En Node 2, editar .env
nano /opt/limpieza/arqCS-NCapas/backend/.env

# Agregar configuración de pool de conexiones
SQLALCHEMY_POOL_SIZE=20
SQLALCHEMY_MAX_OVERFLOW=40
SQLALCHEMY_POOL_RECYCLE=3600
SQLALCHEMY_POOL_TIMEOUT=30

# Reiniciar servicio
sudo systemctl restart limpieza-backend
```

### Optimizar Nginx

```bash
# En Node 3, editar nginx.conf
sudo nano /etc/nginx/nginx.conf

# Aumentar worker processes
worker_processes auto;

# Aumentar worker connections
events {
    worker_connections 4096;
}

# Agregar caching
http {
    proxy_cache_path /var/cache/nginx levels=1:2 keys_zone=my_cache:10m;
    
    # En el bloque server
    location /static {
        proxy_cache my_cache;
        proxy_cache_valid 200 1d;
    }
}

# Reiniciar Nginx
sudo systemctl restart nginx
```

## Seguridad

### Actualizar Contraseñas Regularmente

```bash
# Cambiar contraseña de PostgreSQL cada 90 días
sudo -u postgres psql
ALTER USER limpieza_user WITH PASSWORD 'nueva_contraseña_segura';
```

### Auditoría de Acceso

```bash
# Ver intentos de acceso SSH
sudo grep "Failed password" /var/log/auth.log | wc -l

# Ver IPs que intentan acceder
sudo grep "Failed password" /var/log/auth.log | awk '{print $11}' | sort | uniq -c | sort -rn

# Bloquear IPs sospechosas
sudo ufw deny from IP_SOSPECHOSA
```

### Verificar Integridad de Archivos

```bash
# Crear hash de archivos importantes
sha256sum /opt/limpieza/arqCS-NCapas/backend/app/__init__.py > /opt/hashes.txt

# Verificar integridad
sha256sum -c /opt/hashes.txt
```

## Troubleshooting Común

### Servicio no inicia después de reinicio

```bash
# Verificar que está habilitado
sudo systemctl is-enabled postgresql
sudo systemctl is-enabled limpieza-backend
sudo systemctl is-enabled nginx

# Habilitar si no lo está
sudo systemctl enable postgresql
sudo systemctl enable limpieza-backend
sudo systemctl enable nginx

# Reiniciar manualmente
sudo systemctl start postgresql
sudo systemctl start limpieza-backend
sudo systemctl start nginx
```

### Base de datos crece demasiado

```bash
# En Node 1, ver tamaño de base de datos
sudo -u postgres psql
SELECT datname, pg_size_pretty(pg_database_size(datname)) FROM pg_database;

# Limpiar espacio no utilizado
VACUUM FULL;

# Analizar tablas
ANALYZE;
```

### Rendimiento lento

```bash
# En Node 2, ver queries lentas
sudo journalctl -u limpieza-backend | grep "slow"

# En Node 1, habilitar log de queries lentas
sudo nano /etc/postgresql/*/main/postgresql.conf
log_min_duration_statement = 1000  # 1 segundo

sudo systemctl restart postgresql
```

## Checklist de Mantenimiento

### Mensual
- [ ] Revisar logs de errores
- [ ] Verificar espacio en disco
- [ ] Hacer backup de base de datos
- [ ] Actualizar paquetes del sistema
- [ ] Revisar uso de recursos

### Trimestral
- [ ] Actualizar dependencias
- [ ] Revisar configuración de seguridad
- [ ] Probar restauración de backups
- [ ] Revisar certificados SSL/TLS

### Anual
- [ ] Auditoría de seguridad completa
- [ ] Revisión de arquitectura
- [ ] Planificación de upgrades
- [ ] Documentación actualizada
