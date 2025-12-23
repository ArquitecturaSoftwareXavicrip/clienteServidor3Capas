# Despliegue con Docker - 3 Nodos

## Estado Actual

✅ **Despliegue completado exitosamente con Docker**

Los 3 nodos están corriendo en contenedores Docker:

```
┌─────────────────────────────────────────────────────────┐
│                    RED LOCAL (Docker)                   │
│                                                         │
│  ┌─────────────────┐    ┌─────────────────┐          │
│  │   NODO 1        │    │   NODO 2        │          │
│  │   Tier 3        │    │   Tier 2        │          │
│  │   Database      │◄───┤   Backend       │          │
│  │   PostgreSQL    │    │   Flask API     │          │
│  │ localhost:5433  │    │ localhost:5001  │          │
│  └─────────────────┘    └────────┬────────┘          │
│                                   │                    │
│                                   │ HTTP/REST          │
│                                   ▼                    │
│                          ┌─────────────────┐          │
│                          │   NODO 3        │          │
│                          │   Tier 1        │          │
│                          │   Frontend      │          │
│                          │   React         │          │
│                          │ localhost:3001  │          │
│                          └─────────────────┘          │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

## Configuración de Contenedores

| Contenedor | Servicio | Puerto | Estado |
|-----------|----------|--------|--------|
| limpieza_db | PostgreSQL | 5433 | ✅ Corriendo |
| limpieza_backend | Flask API | 5001 | ✅ Corriendo |
| limpieza_frontend | React | 3001 | ✅ Corriendo |

## Acceso a los Servicios

- **Frontend**: http://localhost:3001
- **Backend API**: http://localhost:5001
- **Database**: localhost:5433 (PostgreSQL)

## Comandos Útiles

### Ver estado de contenedores
```bash
docker ps
```

### Ver logs en tiempo real

**Node 1 (Database)**:
```bash
docker logs limpieza_db -f
```

**Node 2 (Backend)**:
```bash
docker logs limpieza_backend -f
```

**Node 3 (Frontend)**:
```bash
docker logs limpieza_frontend -f
```

### Acceder a la base de datos
```bash
docker exec -it limpieza_db psql -U limpieza_user -d limpieza_empresas
```

Comandos útiles en psql:
```sql
\dt                    -- Ver tablas
SELECT * FROM empresas; -- Ver empresas
SELECT * FROM servicios; -- Ver servicios
SELECT * FROM contratos; -- Ver contratos
\q                     -- Salir
```

### Detener contenedores
```bash
docker-compose down
```

### Reiniciar contenedores
```bash
docker-compose up
```

### Reconstruir imágenes
```bash
docker-compose up --build
```

## Pruebas del Flujo Completo

### 1. Verificar conectividad Backend → Database

```bash
curl -s http://localhost:5001/api/empresas
# Debería devolver: []
```

### 2. Crear una empresa desde el Frontend

1. Abre http://localhost:3001
2. Completa el formulario con:
   - Nombre: Tech Solutions S.A.
   - Dirección: Av. Principal 123
   - Teléfono: 0991234567
   - Email: contacto@techsolutions.com
3. Haz clic en "Crear"

### 3. Verificar que se guardó en la BD

```bash
docker exec limpieza_db psql -U limpieza_user -d limpieza_empresas -c "SELECT * FROM empresas;"
```

Deberías ver la empresa que creaste.

### 4. Verificar logs del Backend

```bash
docker logs limpieza_backend -f
```

Deberías ver logs de la solicitud POST.

## Credenciales de Base de Datos

- **Usuario**: limpieza_user
- **Contraseña**: contraseña_segura_123
- **Base de datos**: limpieza_empresas
- **Host**: database (desde otros contenedores) o localhost (desde tu máquina)
- **Puerto**: 5433

## Estructura de Datos

### Tabla: empresas
```
id | nombre | direccion | telefono | email
```

### Tabla: servicios
```
id | nombre | descripcion | precio_base | duracion_horas
```

### Tabla: contratos
```
id | empresa_id | servicio_id | fecha_inicio | fecha_fin | estado | precio_final
```

## Volúmenes

Los datos de PostgreSQL se almacenan en el volumen `postgres_data` de Docker, que persiste entre reinicios de contenedores.

Para limpiar todo (incluyendo datos):
```bash
docker-compose down -v
```

## Próximos Pasos

1. ✅ Crear empresas desde el frontend
2. ✅ Crear servicios
3. ✅ Crear contratos
4. ✅ Verificar datos en la BD
5. ⏳ Desplegar en 3 máquinas Linux reales (siguiendo guiaDespliegueLocal.md)

## Diferencias con Despliegue en 3 Nodos Reales

| Aspecto | Docker | 3 Nodos Reales |
|--------|--------|----------------|
| Máquinas | 1 (contenedores) | 3 (físicas/virtuales) |
| Red | Docker network | Red local (LAN) |
| IPs | 172.19.0.x | 192.168.1.x |
| Puertos | Mapeados a localhost | Acceso directo |
| Persistencia | Volúmenes Docker | Sistema de archivos |
| Escalabilidad | Limitada | Independiente por tier |

## Troubleshooting

### Puerto ya está en uso
```bash
# Cambiar puerto en docker-compose.yml
# Buscar "5433:5432" y cambiar a otro puerto, ej: "5434:5432"
```

### Contenedor no inicia
```bash
docker logs [nombre_contenedor]
# Ver el error específico
```

### Base de datos vacía
```bash
# Reiniciar con volumen limpio
docker-compose down -v
docker-compose up
```

## Documentación Relacionada

- **guiaDespliegueLocal.md** - Despliegue en 3 nodos Linux reales
- **QUICK_START.md** - Inicio rápido
- **TROUBLESHOOTING.md** - Solución de problemas
- **maintenance-guide.md** - Mantenimiento
