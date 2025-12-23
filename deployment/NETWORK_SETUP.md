# Configuración de Red para Despliegue en 3 Nodos

## Requisitos de Red

### Topología de Red Recomendada

```
┌─────────────────────────────────────────────────────────┐
│                    RED LOCAL (LAN)                      │
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

## Configuración de IPs Estáticas

### En Linux (Ubuntu/Debian)

Para asegurar que los nodos mantienen sus IPs, configura direcciones estáticas:

#### Node 1 (Database)

```bash
# Editar configuración de red
sudo nano /etc/netplan/00-installer-config.yaml
```

Contenido:
```yaml
network:
  version: 2
  ethernets:
    eth0:
      dhcp4: no
      addresses:
        - 192.168.1.10/24
      gateway4: 192.168.1.1
      nameservers:
        addresses: [8.8.8.8, 8.8.4.4]
```

Aplicar cambios:
```bash
sudo netplan apply
sudo ip addr show
```

#### Node 2 (Backend)

```bash
sudo nano /etc/netplan/00-installer-config.yaml
```

Contenido:
```yaml
network:
  version: 2
  ethernets:
    eth0:
      dhcp4: no
      addresses:
        - 192.168.1.20/24
      gateway4: 192.168.1.1
      nameservers:
        addresses: [8.8.8.8, 8.8.4.4]
```

#### Node 3 (Frontend)

```bash
sudo nano /etc/netplan/00-installer-config.yaml
```

Contenido:
```yaml
network:
  version: 2
  ethernets:
    eth0:
      dhcp4: no
      addresses:
        - 192.168.1.30/24
      gateway4: 192.168.1.1
      nameservers:
        addresses: [8.8.8.8, 8.8.4.4]
```

### En macOS

Si estás usando máquinas virtuales en macOS:

1. Abre System Preferences > Network
2. Selecciona la interfaz de red
3. Haz clic en "Advanced..."
4. Ve a la pestaña "TCP/IP"
5. Configura la IP manualmente

## Verificación de Conectividad

### Ping entre Nodos

```bash
# Desde Node 1
ping 192.168.1.20  # Debería responder
ping 192.168.1.30  # Debería responder

# Desde Node 2
ping 192.168.1.10  # Debería responder
ping 192.168.1.30  # Debería responder

# Desde Node 3
ping 192.168.1.10  # Debería responder
ping 192.168.1.20  # Debería responder
```

### Verificar Puertos Abiertos

```bash
# Desde Node 2, verificar que puede conectar a Node 1 en puerto 5432
nc -zv 192.168.1.10 5432

# Desde Node 3, verificar que puede conectar a Node 2 en puerto 5001
nc -zv 192.168.1.20 5001

# Desde tu máquina local
nc -zv 192.168.1.30 3001
```

## Configuración de Firewall

### UFW (Uncomplicated Firewall)

#### Node 1 (Database)

```bash
# Habilitar firewall
sudo ufw enable

# Permitir SSH (importante para no perder acceso)
sudo ufw allow 22/tcp

# Permitir PostgreSQL desde la red local
sudo ufw allow from 192.168.1.0/24 to any port 5432

# Ver estado
sudo ufw status
```

#### Node 2 (Backend)

```bash
# Habilitar firewall
sudo ufw enable

# Permitir SSH
sudo ufw allow 22/tcp

# Permitir Flask API desde la red local
sudo ufw allow from 192.168.1.0/24 to any port 5001

# Ver estado
sudo ufw status
```

#### Node 3 (Frontend)

```bash
# Habilitar firewall
sudo ufw enable

# Permitir SSH
sudo ufw allow 22/tcp

# Permitir Nginx desde la red local
sudo ufw allow from 192.168.1.0/24 to any port 3001
sudo ufw allow 'Nginx Full'

# Ver estado
sudo ufw status
```

### iptables (Alternativa)

Si prefieres usar iptables directamente:

```bash
# Node 1 - Permitir PostgreSQL
sudo iptables -A INPUT -p tcp --dport 5432 -s 192.168.1.0/24 -j ACCEPT
sudo iptables -A INPUT -p tcp --dport 5432 -j DROP

# Node 2 - Permitir Flask
sudo iptables -A INPUT -p tcp --dport 5001 -s 192.168.1.0/24 -j ACCEPT
sudo iptables -A INPUT -p tcp --dport 5001 -j DROP

# Node 3 - Permitir Nginx
sudo iptables -A INPUT -p tcp --dport 3001 -s 192.168.1.0/24 -j ACCEPT
sudo iptables -A INPUT -p tcp --dport 3001 -j DROP

# Guardar configuración
sudo iptables-save | sudo tee /etc/iptables/rules.v4
```

## Resolución de Nombres (DNS)

### Opción 1: Usar /etc/hosts

Para facilitar la comunicación, puedes agregar entradas en `/etc/hosts`:

```bash
# En cada nodo, editar /etc/hosts
sudo nano /etc/hosts
```

Agregar:
```
192.168.1.10    node1-db
192.168.1.20    node2-backend
192.168.1.30    node3-frontend
```

Luego puedes usar nombres en lugar de IPs:
```bash
# En lugar de: psql -h 192.168.1.10
psql -h node1-db -U limpieza_user -d limpieza_empresas
```

### Opción 2: Configurar DNS Local

Si tienes un servidor DNS local, agrega registros A:
```
node1-db.local      192.168.1.10
node2-backend.local 192.168.1.20
node3-frontend.local 192.168.1.30
```

## Pruebas de Conectividad Completas

### Script de Verificación

Crea un script para verificar toda la conectividad:

```bash
#!/bin/bash
# test-connectivity.sh

echo "=== Prueba de Conectividad entre Nodos ==="

# Colores para output
GREEN='\033[0;32m'
RED='\033[0;31m'
NC='\033[0m'

test_connection() {
    if ping -c 1 $1 &> /dev/null; then
        echo -e "${GREEN}✓${NC} Conectado a $1"
    else
        echo -e "${RED}✗${NC} No se puede conectar a $1"
    fi
}

test_port() {
    if nc -zv $1 $2 &> /dev/null; then
        echo -e "${GREEN}✓${NC} Puerto $2 abierto en $1"
    else
        echo -e "${RED}✗${NC} Puerto $2 cerrado en $1"
    fi
}

echo "Pruebas de Ping:"
test_connection 192.168.1.10
test_connection 192.168.1.20
test_connection 192.168.1.30

echo ""
echo "Pruebas de Puertos:"
test_port 192.168.1.10 5432
test_port 192.168.1.20 5001
test_port 192.168.1.30 3001

echo ""
echo "Pruebas de Servicios:"

# PostgreSQL
if psql -h 192.168.1.10 -U limpieza_user -d limpieza_empresas -c "SELECT 1" &> /dev/null; then
    echo -e "${GREEN}✓${NC} PostgreSQL respondiendo"
else
    echo -e "${RED}✗${NC} PostgreSQL no responde"
fi

# Backend
if curl -s http://192.168.1.20:5001/ &> /dev/null; then
    echo -e "${GREEN}✓${NC} Backend respondiendo"
else
    echo -e "${RED}✗${NC} Backend no responde"
fi

# Frontend
if curl -s http://192.168.1.30:3001/ &> /dev/null; then
    echo -e "${GREEN}✓${NC} Frontend respondiendo"
else
    echo -e "${RED}✗${NC} Frontend no responde"
fi
```

Ejecutar:
```bash
chmod +x test-connectivity.sh
./test-connectivity.sh
```

## Optimización de Red

### Aumentar Límites de Conexión

En Node 1 (Database), para soportar más conexiones:

```bash
# Editar limits.conf
sudo nano /etc/security/limits.conf

# Agregar:
postgres soft nofile 65536
postgres hard nofile 65536
postgres soft nproc 65536
postgres hard nproc 65536
```

### Configurar Timeouts

En Node 2 (Backend), para conexiones a la base de datos:

```bash
# En el archivo .env
SQLALCHEMY_POOL_TIMEOUT=30
SQLALCHEMY_POOL_RECYCLE=3600
SQLALCHEMY_POOL_SIZE=10
SQLALCHEMY_MAX_OVERFLOW=20
```

## Monitoreo de Red

### Ver Tráfico de Red

```bash
# Instalar herramientas
sudo apt install nethogs iftop -y

# Ver tráfico por proceso
sudo nethogs

# Ver tráfico por interfaz
sudo iftop
```

### Monitorear Conexiones

```bash
# Ver conexiones activas
netstat -an | grep ESTABLISHED

# Ver conexiones específicas a PostgreSQL
netstat -an | grep 5432

# Ver conexiones específicas a Backend
netstat -an | grep 5001
```

## Seguridad de Red

### Configurar VPN (Opcional)

Para mayor seguridad, considera usar una VPN entre nodos:

```bash
# Instalar OpenVPN
sudo apt install openvpn -y

# Configurar certificados y claves
# (Consulta documentación de OpenVPN)
```

### Usar SSH Tunneling

Para conexiones seguras:

```bash
# Crear túnel SSH para PostgreSQL
ssh -L 5432:192.168.1.10:5432 usuario@192.168.1.10

# Luego conectar localmente
psql -h localhost -U limpieza_user -d limpieza_empresas
```

### Encriptar Conexiones PostgreSQL

```bash
# En postgresql.conf
ssl = on
ssl_cert_file = '/etc/postgresql/server.crt'
ssl_key_file = '/etc/postgresql/server.key'
```

## Tabla de Referencia de Puertos

| Nodo | Servicio | Puerto | Protocolo | Acceso |
|------|----------|--------|-----------|--------|
| Node 1 | PostgreSQL | 5432 | TCP | 192.168.1.0/24 |
| Node 2 | Flask API | 5001 | TCP | 192.168.1.0/24 |
| Node 3 | Nginx | 3001 | TCP | 192.168.1.0/24 |
| Todos | SSH | 22 | TCP | Según política |
