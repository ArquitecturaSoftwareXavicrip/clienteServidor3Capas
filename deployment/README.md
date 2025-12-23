# Despliegue en 3 Nodos - Arquitectura de 3 Capas

Este directorio contiene todos los scripts y documentación necesarios para desplegar la aplicación "Servicios de Limpieza para Empresas" en una arquitectura de 3 nodos separados.

## 📋 Contenido

### Scripts de Configuración
- **`node1-database-setup.sh`** - Configuración de PostgreSQL en Node 1
- **`node2-backend-setup.sh`** - Configuración de Flask API en Node 2
- **`node3-frontend-setup.sh`** - Configuración de React App en Node 3
- **`verify-deployment.sh`** - Script de verificación del despliegue

### Documentación
- **`README.md`** - Este archivo
- **`QUICK_START.md`** - Guía rápida de inicio
- **`DEPLOYMENT_CHECKLIST.md`** - Checklist completo de despliegue
- **`NETWORK_SETUP.md`** - Configuración de red y firewall
- **`TROUBLESHOOTING.md`** - Solución de problemas comunes

## 🏗️ Arquitectura

```
┌─────────────────────────────────────────────────────────┐
│                    RED LOCAL                            │
│                                                         │
│  ┌─────────────────┐    ┌─────────────────┐          │
│  │   NODO 1        │    │   NODO 2        │          │
│  │   Tier 3        │    │   Tier 2        │          │
│  │   Database      │◄───┤   Backend       │          │
│  │   IP: 192.168.1.10│    │   IP: 192.168.1.20│          │
│  │   Puerto: 5432  │    │   Puerto: 5001  │          │
│  └─────────────────┘    └────────┬────────┘          │
│                                   │                    │
│                                   │ HTTP/REST          │
│                                   ▼                    │
│                          ┌─────────────────┐          │
│                          │   NODO 3        │          │
│                          │   Tier 1        │          │
│                          │   Frontend      │          │
│                          │   IP: 192.168.1.30│          │
│                          │   Puerto: 3001  │          │
│                          └─────────────────┘          │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

## 📊 Especificaciones de los Nodos

| Nodo | Capa | IP | Puerto | Servicio | SO |
|------|------|----|--------|----------|-----|
| Node 1 | Tier 3 (Data) | 192.168.1.10 | 5432 | PostgreSQL | Linux |
| Node 2 | Tier 2 (Logic) | 192.168.1.20 | 5001 | Flask API | Linux |
| Node 3 | Tier 1 (UI) | 192.168.1.30 | 3001 | React + Nginx | Linux |

## 🚀 Inicio Rápido

### Opción 1: Despliegue Automático

```bash
# En cada nodo, ejecutar el script correspondiente
# Node 1
ssh usuario@192.168.1.10
bash node1-database-setup.sh

# Node 2
ssh usuario@192.168.1.20
bash node2-backend-setup.sh

# Node 3
ssh usuario@192.168.1.30
bash node3-frontend-setup.sh
```

### Opción 2: Despliegue Manual

Sigue los pasos detallados en `QUICK_START.md`

## ✅ Verificación

Después del despliegue, verifica que todo funciona:

```bash
# Ejecutar script de verificación
bash verify-deployment.sh
```

O verifica manualmente:

```bash
# Desde tu máquina local
curl http://192.168.1.20:5001/          # Backend
curl http://192.168.1.30:3001/          # Frontend

# Desde Node 2
psql -h 192.168.1.10 -U limpieza_user -d limpieza_empresas

# Desde Node 3
curl http://192.168.1.20:5001/api/empresas
```

## 📝 Configuración

### Variables de Entorno

Antes de ejecutar los scripts, asegúrate de que las IPs en los archivos `.env` sean correctas:

**Backend (.env)**:
```env
SQLALCHEMY_DATABASE_URI=postgresql://limpieza_user:contraseña_segura_123@192.168.1.10:5432/limpieza_empresas
CORS_ORIGINS=http://192.168.1.30:3001
```

**Frontend (.env)**:
```env
REACT_APP_API_URL=http://192.168.1.20:5001/api
```

### Cambiar IPs

Si tus IPs son diferentes, edita los scripts antes de ejecutarlos:

```bash
# En los scripts, busca y reemplaza:
# 192.168.1.10 -> Tu IP de Node 1
# 192.168.1.20 -> Tu IP de Node 2
# 192.168.1.30 -> Tu IP de Node 3

sed -i 's/192.168.1.10/TU_IP_NODE1/g' node1-database-setup.sh
sed -i 's/192.168.1.20/TU_IP_NODE2/g' node2-backend-setup.sh
sed -i 's/192.168.1.30/TU_IP_NODE3/g' node3-frontend-setup.sh
```

## 🔍 Monitoreo

### Ver Logs en Tiempo Real

```bash
# Node 1 (Database)
ssh usuario@192.168.1.10 "sudo journalctl -u postgresql -f"

# Node 2 (Backend)
ssh usuario@192.168.1.20 "sudo journalctl -u limpieza-backend -f"

# Node 3 (Frontend)
ssh usuario@192.168.1.30 "sudo tail -f /var/log/nginx/access.log"
```

### Verificar Estado de Servicios

```bash
# Node 1
ssh usuario@192.168.1.10 "sudo systemctl status postgresql"

# Node 2
ssh usuario@192.168.1.20 "sudo systemctl status limpieza-backend"

# Node 3
ssh usuario@192.168.1.30 "sudo systemctl status nginx"
```

## 🛠️ Solución de Problemas

Consulta `TROUBLESHOOTING.md` para soluciones detalladas de problemas comunes.

Problemas frecuentes:
- **No puedo conectar entre nodos** → Ver `NETWORK_SETUP.md`
- **Backend no inicia** → Ver logs: `sudo journalctl -u limpieza-backend -n 50`
- **Frontend no carga** → Verificar build: `ls /opt/limpieza/arqCS-NCapas/frontend/build/`
- **CORS error** → Verificar CORS_ORIGINS en `.env` del backend

## 📚 Documentación Completa

Para información más detallada, consulta:
- **`QUICK_START.md`** - Pasos rápidos de despliegue
- **`DEPLOYMENT_CHECKLIST.md`** - Checklist completo
- **`NETWORK_SETUP.md`** - Configuración de red
- **`TROUBLESHOOTING.md`** - Solución de problemas

## 🔐 Seguridad

### Cambiar Contraseñas

Antes de desplegar en producción, cambia:

1. **Contraseña de PostgreSQL**:
   ```bash
   # En Node 1
   sudo -u postgres psql
   ALTER USER limpieza_user WITH PASSWORD 'nueva_contraseña_segura';
   ```

2. **SECRET_KEY de Flask**:
   ```bash
   # En Node 2, editar .env
   SECRET_KEY=tu-clave-secreta-muy-segura-aqui
   ```

### Certificados SSL/TLS

Para producción, configura HTTPS:

```bash
# En Node 3
sudo apt install certbot python3-certbot-nginx -y
sudo certbot --nginx -d tu-dominio.com
```

## 📞 Soporte

Si encuentras problemas:

1. Consulta `TROUBLESHOOTING.md`
2. Verifica los logs de cada servicio
3. Ejecuta `verify-deployment.sh` para diagnósticos
4. Revisa la documentación de cada componente

## 📄 Licencia

Este proyecto es parte de la arquitectura de 3 capas para educación.

## 🎯 Próximos Pasos

Después de un despliegue exitoso:

1. **Configurar Monitoreo**
   - Instalar Prometheus/Grafana
   - Configurar alertas

2. **Backups Automáticos**
   - Configurar pg_dump automático
   - Almacenar en ubicación segura

3. **Escalabilidad**
   - Agregar múltiples instancias del backend
   - Configurar balanceador de carga

4. **Seguridad**
   - Configurar SSL/TLS
   - Implementar autenticación
   - Configurar WAF

---

**Última actualización**: Diciembre 2024
**Versión**: 1.0
