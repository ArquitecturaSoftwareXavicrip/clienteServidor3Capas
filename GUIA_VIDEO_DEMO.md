# 🎬 Guía para Video: Demostración Arquitectura 3 Capas en 3 Nodos

## 🎯 Objetivo del Video

Demostrar la arquitectura de 3 capas con **separación física** donde:
1. **Computadora 1 (Frontend)**: Usuario crea una solicitud de permiso
2. **Computadora 2 (Base de Datos)**: Se ve el cambio en tiempo real en PostgreSQL
3. **Computadora 3 (Backend)**: Procesa la solicitud (puede ser la misma que BD)

---

## 🖥️ Escenarios de Demostración

### Escenario A: 3 Computadoras Reales (Ideal)

```
┌─────────────────┐       ┌─────────────────┐       ┌─────────────────┐
│   COMPU 1       │       │   COMPU 2       │       │   COMPU 3       │
│   Frontend      │ ────> │   Backend       │ ────> │   PostgreSQL    │
│   192.168.1.30  │       │   192.168.1.20  │       │   192.168.1.10  │
│   Puerto: 3001  │       │   Puerto: 5001  │       │   Puerto: 5432  │
└─────────────────┘       └─────────────────┘       └─────────────────┘
```

### Escenario B: 2 Computadoras (Práctico)

```
┌─────────────────┐       ┌──────────────────────────┐
│   COMPU 1       │       │   COMPU 2                │
│   Frontend      │ ────> │   Backend + PostgreSQL   │
│   192.168.1.30  │       │   192.168.1.20           │
│   Puerto: 3001  │       │   Puertos: 5001, 5432    │
└─────────────────┘       └──────────────────────────┘
```

### Escenario C: 1 Computadora + Navegador Remoto (Alternativa)

```
┌────────────────────────────────────────────┐
│   COMPU 1 (Servidor)                       │
│   Backend + PostgreSQL                     │
│   192.168.1.20                             │
│   Puertos: 5001, 5432                      │
└──────────────┬─────────────────────────────┘
               │
         ┌─────┴─────┐
         │           │
    [Laptop 1]   [Laptop 2]
    Frontend     psql
    navegador    terminal
```

---

## 🎬 GUIÓN DEL VIDEO (Escenario B - 2 Computadoras)

### Preparación Previa (Antes de Grabar)

#### COMPU 1: Frontend (Tu laptop)
- IP: Obtener con `ipconfig` (ej: 192.168.1.30)
- Sistema: Windows
- Solo necesita navegador web

#### COMPU 2: Backend + BD (Otra computadora/VM)
- IP: Obtener con `ifconfig` o `ip addr` (ej: 192.168.1.20)
- Sistema: Linux (Ubuntu) o Windows con PostgreSQL
- Necesita: PostgreSQL, Python, código del backend

---

## 📋 SETUP PREVIO (COMPU 2: Backend + BD)

### Paso 1: Instalar PostgreSQL

```bash
# Ubuntu/Linux
sudo apt update
sudo apt install postgresql postgresql-contrib -y

# Iniciar PostgreSQL
sudo systemctl start postgresql
sudo systemctl enable postgresql
```

### Paso 2: Configurar PostgreSQL

```bash
# Crear base de datos
sudo -u postgres psql -c "CREATE DATABASE limpieza_empresas;"

# Crear tablas
cd /ruta/al/proyecto/database
sudo -u postgres psql limpieza_empresas -f schema.sql

# Configurar acceso remoto
sudo nano /etc/postgresql/15/main/postgresql.conf
# Cambiar: listen_addresses = '*'

sudo nano /etc/postgresql/15/main/pg_hba.conf
# Agregar: host all all 192.168.1.0/24 trust

# Reiniciar
sudo systemctl restart postgresql
```

### Paso 3: Configurar Backend

```bash
# Clonar proyecto
git clone https://github.com/samuelanyoneai/clienteServidor3Capas.git
cd clienteServidor3Capas/backend

# Crear entorno virtual
python3 -m venv venv
source venv/bin/activate

# Instalar dependencias
pip install -r requirements.txt
pip install psycopg2-binary

# Crear .env
cat > .env << EOF
FLASK_ENV=production
PORT=5001
SECRET_KEY=demo-key
SQLALCHEMY_DATABASE_URI=postgresql://postgres@localhost:5432/limpieza_empresas
CORS_ORIGINS=http://192.168.1.30:3001,http://192.168.1.0/24
EOF

# Iniciar backend
python run.py
```

### Paso 4: Cargar Datos Iniciales

```bash
cd database
python3 init_db.py
python3 init_permisos.py
python3 init_empleados.py
```

---

## 🎥 GUIÓN DEL VIDEO

### Parte 1: Introducción (30 segundos)

**[Pantalla: Diagrama de arquitectura]**

**Narración:**
> "Hoy vamos a demostrar una arquitectura de 3 capas con separación física de componentes. Tenemos el frontend en una computadora, el backend en otra, y ambas conectadas a PostgreSQL."

**[Mostrar:]**
- Diagrama de 3 capas
- IPs de cada nodo

---

### Parte 2: Mostrar el Estado Inicial (1 minuto)

**[COMPU 2: Terminal con psql]**

```bash
# Mostrar conexión a PostgreSQL
psql -U postgres -d limpieza_empresas

# Mostrar permisos actuales
SELECT id, empleado, estado, fecha_inicio, fecha_fin 
FROM permisos 
ORDER BY id;
```

**Narración:**
> "Actualmente tenemos 6 permisos en la base de datos. Vamos a crear uno nuevo desde otra computadora."

**[Contar los registros]**
```sql
SELECT COUNT(*) FROM permisos;
-- Resultado: 6
```

**[Salir pero dejar terminal visible]**
```sql
\q
```

---

### Parte 3: Crear Permiso desde COMPU 1 (2 minutos)

**[COMPU 1: Navegador]**

**Abrir:** `http://192.168.1.20:5001/api/permisos` (para mostrar API)

**Narración:**
> "Desde esta computadora accedemos al frontend que se comunica con el backend en la otra máquina."

**Abrir:** `http://192.168.1.20:3001` (o usar el frontend local)

**[Navegar a Permisos]**

**Narración:**
> "Vamos a crear una nueva solicitud de vacaciones."

**[Llenar el formulario:]**
```
Empleado: Samuel Reyes
Tipo: Vacaciones
Fecha Inicio: [Hoy + 7 días]
Fecha Fin: [Hoy + 14 días]
Días Solicitados: 7
Observaciones: Vacaciones familiares - Demo en vivo
```

**[Hacer clic en "Crear"]**

**Narración:**
> "Al hacer clic en crear, la solicitud viaja desde esta computadora, pasa por el backend en la otra máquina, y se guarda en PostgreSQL."

---

### Parte 4: Verificar en Base de Datos (1 minuto)

**[COMPU 2: Terminal psql - Split screen con COMPU 1]**

```bash
# Conectar a PostgreSQL
psql -U postgres -d limpieza_empresas

# Mostrar TODOS los permisos (ahora debería haber 7)
SELECT id, empleado, estado, fecha_inicio, fecha_fin, observaciones 
FROM permisos 
ORDER BY id DESC 
LIMIT 3;
```

**Narración:**
> "Y aquí está! El permiso se guardó instantáneamente en la base de datos en la otra computadora. Ahora tenemos 7 permisos."

**[Resaltar el nuevo registro]**

---

### Parte 5: Aprobar el Permiso (1 minuto)

**[COMPU 1: Navegador]**

**Narración:**
> "Ahora vamos a aprobar este permiso desde el frontend."

**[Hacer clic en "Aprobar" en el permiso recién creado]**

**[Confirmar]**

**Narración:**
> "El estado cambia a aprobado con un indicador visual verde."

---

### Parte 6: Verificar la Aprobación en BD (30 segundos)

**[COMPU 2: Terminal psql]**

```sql
# Ver el cambio de estado
SELECT id, empleado, estado, observaciones 
FROM permisos 
WHERE id = 7;  -- Ajustar al ID correcto
```

**Narración:**
> "Y en tiempo real vemos que el estado cambió a 'aprobado' en la base de datos."

---

### Parte 7: Demostrar Arquitectura (1 minuto)

**[Split screen de ambas computadoras]**

**[COMPU 2: Mostrar logs del backend]**
```bash
# Ver logs en tiempo real
tail -f /ruta/logs/backend.log
# O si usas systemd:
sudo journalctl -u limpieza-backend -f
```

**[COMPU 1: Crear otro permiso]**

**[COMPU 2: Mostrar logs recibiendo la petición]**

**Narración:**
> "Aquí podemos ver cómo cada petición del frontend llega al backend, pasa por las validaciones, y finalmente se guarda en PostgreSQL. Esta es la arquitectura de 3 capas en acción."

---

### Parte 8: Conclusión (30 segundos)

**[Pantalla: Diagrama de arquitectura con checks]**

**Narración:**
> "Hemos demostrado exitosamente una arquitectura de 3 capas con separación física: Frontend en una computadora, Backend en otra, y PostgreSQL como base de datos compartida. Cada capa es independiente y puede escalarse por separado."

---

## 🛠️ CONFIGURACIÓN TÉCNICA PARA EL VIDEO

### COMPU 1 (Frontend) - Tu Laptop

#### Opción A: Acceder al frontend del servidor

```
Abrir navegador en:
http://192.168.1.20:3001
```

#### Opción B: Ejecutar frontend local apuntando al backend remoto

```powershell
cd frontend

# Crear .env apuntando al backend remoto
@"
REACT_APP_API_URL=http://192.168.1.20:5001/api
PORT=3001
"@ | Out-File -FilePath .env -Encoding utf8

npm start

# Abrir: http://localhost:3001
```

---

### COMPU 2 (Backend + BD) - Servidor/VM

```bash
# Terminal 1: Backend corriendo
cd backend
source venv/bin/activate
python run.py

# Terminal 2: PostgreSQL listo para consultas
psql -U postgres -d limpieza_empresas

# Terminal 3: Ver logs en tiempo real (opcional)
tail -f backend.log
```

---

## 📱 TIPS PARA GRABAR EL VIDEO

### Herramientas Recomendadas:
- **OBS Studio** (gratis) - Para grabar pantalla
- **Zoom** - Para split screen de 2 computadoras
- **Microsoft Teams** - Compartir pantalla

### Configuración de Pantalla:

#### Opción 1: Split Screen
```
┌────────────────┬────────────────┐
│   COMPU 1      │   COMPU 2      │
│   Frontend     │   PostgreSQL   │
│   (Navegador)  │   (Terminal)   │
└────────────────┴────────────────┘
```

#### Opción 2: Picture-in-Picture
```
┌──────────────────────────────────┐
│         COMPU 1 Frontend         │
│         (Pantalla completa)      │
│                                  │
│  ┌──────────────┐               │
│  │  COMPU 2     │               │
│  │  Terminal    │               │
│  │  (Esquina)   │               │
│  └──────────────┘               │
└──────────────────────────────────┘
```

---

## 🎭 SCRIPT DETALLADO PARA NARRACIÓN

### Inicio (0:00 - 0:30)

**Visual:** Diagrama de arquitectura

**Texto:**
> "Bienvenidos. Hoy vamos a demostrar una arquitectura de 3 capas Cliente-Servidor con separación física de componentes."
>
> "Tenemos el Tier 1 (Presentación) en una computadora, el Tier 2 (Lógica de Negocio) en otra, y el Tier 3 (Base de Datos) en PostgreSQL."

---

### Estado Inicial (0:30 - 1:00)

**Visual:** COMPU 2 - Terminal psql

**Comandos a ejecutar:**
```sql
-- Mostrar tabla de permisos
\dt

-- Contar permisos actuales
SELECT COUNT(*) as total_permisos FROM permisos;

-- Mostrar últimos 3 permisos
SELECT id, empleado, estado, dias_solicitados 
FROM permisos 
ORDER BY id DESC 
LIMIT 3;
```

**Texto:**
> "Aquí en la Computadora 2 tenemos PostgreSQL con nuestra base de datos. Actualmente tenemos 6 permisos registrados."

---

### Crear Solicitud (1:00 - 2:30)

**Visual:** COMPU 1 - Navegador

**Acciones:**
1. Abrir `http://192.168.1.20:3001`
2. Clic en "Permisos"
3. Llenar formulario:
   - Empleado: "Tu Nombre Completo"
   - Fecha Inicio: [Seleccionar]
   - Fecha Fin: [Seleccionar]
   - Días: 7
   - Observaciones: "Demo de arquitectura 3 capas en vivo"
4. Clic en "Crear"
5. Mostrar mensaje de éxito

**Texto:**
> "Desde la Computadora 1, voy a crear una nueva solicitud de vacaciones."
>
> "Lleno el formulario con mis datos: nombre, fechas, días solicitados."
>
> "Al hacer clic en Crear, esta petición HTTP viaja por la red local hasta el backend en la Computadora 2."

---

### Verificar Inserción (2:30 - 3:00)

**Visual:** COMPU 2 - Terminal psql (sin cerrar la sesión anterior)

**Comandos:**
```sql
-- Actualizar la consulta
SELECT id, empleado, estado, fecha_inicio, dias_solicitados, observaciones
FROM permisos 
ORDER BY id DESC 
LIMIT 1;

-- Contar nuevamente
SELECT COUNT(*) FROM permisos;
-- Ahora debería ser 7
```

**Texto:**
> "Y aquí está el registro en la base de datos! El permiso se guardó exitosamente."
>
> "Como pueden ver, ahora tenemos 7 permisos en lugar de 6."

---

### Aprobar Permiso (3:00 - 3:30)

**Visual:** COMPU 1 - Navegador

**Acciones:**
1. Buscar el permiso recién creado (debería estar en estado PENDIENTE 🟡)
2. Clic en "Aprobar"
3. Confirmar
4. Ver que el estado cambia a APROBADO 🟢

**Texto:**
> "Ahora voy a aprobar este permiso desde el frontend."
>
> "El estado cambia inmediatamente a 'Aprobado' con un indicador verde."

---

### Verificar Actualización (3:30 - 4:00)

**Visual:** COMPU 2 - Terminal psql

**Comandos:**
```sql
-- Ver el cambio de estado
SELECT id, empleado, estado, observaciones 
FROM permisos 
WHERE empleado LIKE '%Tu Nombre%';

-- Ver historial de cambios (si tienes timestamps)
SELECT id, empleado, estado, TO_CHAR(NOW(), 'HH24:MI:SS') as hora_consulta
FROM permisos 
ORDER BY id DESC 
LIMIT 3;
```

**Texto:**
> "Y aquí en la base de datos vemos que el estado cambió a 'aprobado' en tiempo real."
>
> "Esto demuestra la comunicación entre las 3 capas de nuestra arquitectura."

---

### Demostrar Filtros (4:00 - 4:30)

**Visual:** COMPU 1 - Navegador

**Acciones:**
1. Usar el filtro "Filtrar por estado"
2. Seleccionar "Aprobados"
3. Mostrar que solo aparecen los aprobados
4. Seleccionar "Pendientes"
5. Mostrar solo pendientes

**Texto:**
> "El frontend también permite filtrar por estado. Esto se hace mediante una petición al backend que consulta PostgreSQL con un filtro WHERE."

---

### Ver Consulta en BD (4:30 - 5:00)

**Visual:** COMPU 2 - Terminal psql

**Comandos:**
```sql
-- Mostrar cómo se ven solo los aprobados
SELECT id, empleado, estado 
FROM permisos 
WHERE estado = 'aprobado';

-- Mostrar solo pendientes
SELECT id, empleado, estado 
FROM permisos 
WHERE estado = 'pendiente';
```

**Texto:**
> "Estas son las mismas consultas SQL que el backend ejecuta cuando filtramos desde el frontend."

---

### Mostrar Logs del Backend (5:00 - 5:30)

**Visual:** COMPU 2 - Terminal con logs

```bash
# Ver logs en tiempo real
sudo journalctl -u limpieza-backend -f --since "5 minutes ago"

# O si lo ejecutas manualmente:
# Los logs aparecen en la consola donde corre el backend
```

**[COMPU 1: Crear otro permiso mientras se ven los logs]**

**Texto:**
> "Aquí podemos ver los logs del backend procesando cada petición HTTP que llega desde el frontend."

---

### Conclusión (5:30 - 6:00)

**Visual:** Diagrama de arquitectura con animación de flujo

**Texto:**
> "Hemos demostrado exitosamente:"
> 
> "✅ Tier 1: Frontend en una computadora mostrando la interfaz"
>
> "✅ Tier 2: Backend en otra computadora procesando la lógica de negocio"
>
> "✅ Tier 3: PostgreSQL guardando los datos de forma persistente"
>
> "Esta separación permite escalar cada capa independientemente y desplegarlas en diferentes servidores físicos."

---

## 📝 COMANDOS DE MONITOREO EN TIEMPO REAL

### En COMPU 2 - Para el Video

#### Terminal 1: PostgreSQL en Modo Watch

```bash
# Crear script de monitoreo
cat > watch_permisos.sh << 'EOF'
#!/bin/bash
while true; do
    clear
    echo "=== PERMISOS EN TIEMPO REAL ==="
    echo "Hora: $(date '+%H:%M:%S')"
    psql -U postgres -d limpieza_empresas -c "
    SELECT id, empleado, estado, dias_solicitados 
    FROM permisos 
    ORDER BY id DESC 
    LIMIT 5;"
    sleep 2
done
EOF

chmod +x watch_permisos.sh
./watch_permisos.sh
```

Esto actualizará la consulta cada 2 segundos automáticamente.

#### Terminal 2: Backend con Logs Verbosos

```bash
# Ejecutar backend con logs visibles
cd backend
source venv/bin/activate
python run.py

# O ver logs en tiempo real:
tail -f backend.log
```

---

## 🎬 CONFIGURACIÓN ALTERNATIVA: TODO EN DOCKER

Si prefieres usar Docker para la demo:

### COMPU 2 (Servidor):

```bash
# Iniciar todo
docker compose up --build -d

# Cargar datos
docker exec limpieza_backend python ../database/init_db.py
docker exec limpieza_backend python ../database/init_permisos.py
docker exec limpieza_backend python ../database/init_empleados.py

# Monitoreo en tiempo real
docker exec -it limpieza_db psql -U postgres -d limpieza_empresas

# En otra terminal, logs del backend
docker compose logs -f backend
```

### COMPU 1 (Cliente):

Abrir navegador en: `http://192.168.1.20:3001`

---

## 📊 DATOS PARA CREAR EN EL VIDEO

### Permiso 1 (Ejemplo realista):
```
Empleado: María García
Tipo: Vacaciones
Fecha Inicio: 2025-01-15
Fecha Fin: 2025-01-22
Días: 7
Observaciones: Vacaciones de verano - Creado en demo en vivo
```

### Permiso 2 (Para aprobar):
```
Empleado: Carlos López
Tipo: Vacaciones
Fecha Inicio: 2025-02-01
Fecha Fin: 2025-02-10
Días: 9
Observaciones: Viaje familiar - Demo arquitectura 3 capas
```

---

## 🎥 CHECKLIST PRE-GRABACIÓN

### COMPU 2 (Servidor):
- [ ] PostgreSQL instalado y corriendo
- [ ] Base de datos creada y con tablas
- [ ] Backend corriendo en http://0.0.0.0:5001
- [ ] Datos de ejemplo cargados (6 permisos iniciales)
- [ ] Terminal psql abierta y lista
- [ ] Logs del backend visibles

### COMPU 1 (Cliente):
- [ ] Navegador abierto
- [ ] URL del backend/frontend configurada
- [ ] Frontend accesible
- [ ] Datos de prueba preparados

### Ambas Computadoras:
- [ ] Conectadas a la misma red local
- [ ] IPs verificadas
- [ ] Firewall permite conexiones
- [ ] Internet funcionando (para grabar/subir)

### Grabación:
- [ ] OBS/software de grabación configurado
- [ ] Audio de micrófono funcionando
- [ ] Pantallas compartidas/duplicadas
- [ ] Script de narración revisado

---

## 🔍 CONSULTAS SQL ÚTILES PARA EL VIDEO

```sql
-- Mostrar todos los permisos con formato bonito
SELECT 
    id as ID,
    empleado as Empleado,
    estado as Estado,
    dias_solicitados as Días,
    fecha_inicio as Inicio
FROM permisos 
ORDER BY id;

-- Contar por estado
SELECT 
    estado, 
    COUNT(*) as cantidad 
FROM permisos 
GROUP BY estado;

-- Ver el último permiso creado
SELECT * FROM permisos 
ORDER BY id DESC 
LIMIT 1;

-- Monitoreo continuo (copiar y pegar repetidamente)
SELECT NOW() as hora, COUNT(*) as total FROM permisos;
```

---

## 🎯 PUNTOS CLAVE PARA ENFATIZAR

1. **Separación Física**: 
   - "El frontend está en ESTA computadora"
   - "El backend en AQUELLA computadora"
   - "La base de datos es compartida"

2. **Comunicación por Red**:
   - "La petición viaja por HTTP a través de la red local"
   - "El backend se comunica con PostgreSQL por SQL"

3. **Independencia**:
   - "Cada capa es independiente"
   - "Podemos actualizar una sin afectar las otras"
   - "Podemos escalar cada una por separado"

4. **Tiempo Real**:
   - "Los cambios son instantáneos"
   - "Múltiples usuarios podrían usar el sistema simultáneamente"

---

## 📹 ESTRUCTURA DEL VIDEO (6 minutos)

| Tiempo | Sección | Visual |
|--------|---------|--------|
| 0:00-0:30 | Introducción | Diagrama |
| 0:30-1:00 | Estado inicial BD | Terminal psql |
| 1:00-2:30 | Crear permiso | Navegador |
| 2:30-3:00 | Verificar en BD | Terminal psql |
| 3:00-3:30 | Aprobar permiso | Navegador |
| 3:30-4:00 | Verificar cambio | Terminal psql |
| 4:00-4:30 | Filtros | Navegador |
| 4:30-5:00 | Consultas SQL | Terminal psql |
| 5:00-5:30 | Logs backend | Terminal logs |
| 5:30-6:00 | Conclusión | Diagrama |

---

## ✅ RESULTADO ESPERADO

Al final del video habrás demostrado:
- ✅ Arquitectura de 3 capas funcionando
- ✅ Separación física de componentes
- ✅ Comunicación entre capas por red
- ✅ Base de datos centralizada (PostgreSQL)
- ✅ Frontend interactivo
- ✅ Backend procesando lógica de negocio
- ✅ Cambios en tiempo real
- ✅ Sistema CRUD completo

---

## 🚀 BONUS: Demostrar Empleados También

Si tienes tiempo extra (2 minutos más):

1. Navegar a "Empleados"
2. Crear un empleado
3. Verificar en BD:
   ```sql
   SELECT * FROM empleados ORDER BY id DESC LIMIT 1;
   ```

Esto demuestra que el sistema es extensible y sigue el mismo patrón.

---

¡Buena suerte con tu video! 🎬

