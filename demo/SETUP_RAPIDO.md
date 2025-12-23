# ⚡ Setup Rápido para Video Demo

## 🎯 Objetivo

Configurar 2 computadoras para demostrar arquitectura de 3 capas en video.

---

## 🖥️ CONFIGURACIÓN: 2 Computadoras

### Opción Recomendada:

```
COMPU 1 (Tu Laptop)              COMPU 2 (Servidor/VM)
    Frontend                     Backend + PostgreSQL
    Navegador                    Terminal
    192.168.1.30                 192.168.1.20
```

---

## ⚡ SETUP ULTRA RÁPIDO

### COMPU 2 (Servidor - Linux)

```bash
# 1. Clonar proyecto
git clone https://github.com/samuelanyoneai/clienteServidor3Capas.git
cd clienteServidor3Capas

# 2. Ejecutar con Docker (LO MÁS FÁCIL)
docker compose up --build -d

# 3. Esperar y cargar datos
sleep 15
docker exec limpieza_backend python ../database/init_db.py
docker exec limpieza_backend python ../database/init_permisos.py
docker exec limpieza_backend python ../database/init_empleados.py

# 4. Verificar IP
hostname -I
# Ejemplo: 192.168.1.20

# 5. Abrir terminal para monitorear BD
docker exec -it limpieza_db psql -U postgres -d limpieza_empresas
```

**¡LISTO!** Backend y BD corriendo en Docker.

---

### COMPU 1 (Tu Laptop - Windows)

```powershell
# Opción 1: Acceder vía navegador al frontend del servidor
# Abrir navegador en:
http://192.168.1.20:3001

# Opción 2: Ejecutar frontend local apuntando al servidor
cd clienteServidor3Capas\frontend

# Crear .env
@"
REACT_APP_API_URL=http://192.168.1.20:5001/api
PORT=3001
"@ | Out-File -FilePath .env -Encoding utf8

npm install
npm start

# Abrir: http://localhost:3001
```

---

## 🎬 GUIÓN DEL VIDEO (5 minutos)

### Minuto 1: Introducción
**[Pantalla: PowerPoint con diagrama]**
- Explicar arquitectura de 3 capas
- Mostrar que cada capa está en diferente nodo

### Minuto 2: Estado Inicial
**[COMPU 2: Terminal]**
```sql
SELECT COUNT(*) FROM permisos;
SELECT id, empleado, estado FROM permisos ORDER BY id;
```

### Minuto 3: Crear Permiso
**[COMPU 1: Navegador]**
- Navegar a Permisos
- Crear nuevo permiso
- Mostrar mensaje de éxito

### Minuto 4: Verificar en BD
**[COMPU 2: Terminal - ejecutar nuevamente]**
```sql
SELECT * FROM permisos ORDER BY id DESC LIMIT 1;
SELECT COUNT(*) FROM permisos;
```

### Minuto 5: Aprobar y Verificar
**[COMPU 1: Aprobar el permiso]**
**[COMPU 2: Ver cambio de estado en BD]**
```sql
SELECT id, empleado, estado FROM permisos WHERE id = 7;
```

---

## 📋 COMANDOS SQL PARA EL VIDEO

### Mostrar en Pantalla Grande:

```sql
-- Al inicio del video
SELECT 
    id, 
    empleado, 
    estado,
    dias_solicitados as días
FROM permisos 
ORDER BY id;

-- Después de crear
SELECT COUNT(*) as total FROM permisos;

-- Ver el nuevo
SELECT * FROM permisos ORDER BY id DESC LIMIT 1;

-- Ver cambio de estado
SELECT id, empleado, estado 
FROM permisos 
WHERE estado = 'aprobado' 
ORDER BY id DESC;
```

---

## 🎥 TIPS PARA GRABAR

### Grabación de Pantalla:
1. **OBS Studio** (gratis): https://obsproject.com/
2. Configurar 2 escenas:
   - Escena 1: COMPU 1 (Navegador)
   - Escena 2: COMPU 2 (Terminal)
3. Alternar entre escenas según el guión

### Layout Recomendado:
```
┌─────────────────────┬──────────────────┐
│   COMPU 1           │   COMPU 2        │
│   Frontend          │   PostgreSQL     │
│   (70% pantalla)    │   (30% pantalla) │
└─────────────────────┴──────────────────┘
```

### Configuración de Audio:
- Micrófono para narración
- Audio del sistema (opcional)

---

## ✅ CHECKLIST PRE-GRABACIÓN

### COMPU 2 (Servidor):
- [ ] Docker Desktop corriendo (o PostgreSQL + Backend manual)
- [ ] `docker compose ps` muestra todos UP
- [ ] Backend responde: `curl http://localhost:5001/`
- [ ] PostgreSQL accesible: `psql -U postgres -d limpieza_empresas`
- [ ] 6 permisos iniciales cargados
- [ ] Terminal psql abierta y lista

### COMPU 1 (Cliente):
- [ ] Navegador abierto
- [ ] Frontend accesible
- [ ] Puede ver permisos
- [ ] Datos de prueba preparados

### Grabación:
- [ ] OBS configurado
- [ ] Micrófono funcionando
- [ ] Script de narración revisado
- [ ] Hacer prueba de 1 minuto primero

---

## 🚀 INICIO RÁPIDO DEL VIDEO

### Antes de Grabar:

```bash
# COMPU 2: Reiniciar servicios
docker compose restart

# Verificar estado
docker compose ps

# Abrir terminal de monitoreo
docker exec -it limpieza_db psql -U postgres -d limpieza_empresas
```

```powershell
# COMPU 1: Abrir frontend
Start-Process "http://192.168.1.20:3001"
```

### Durante la Grabación:

**[Iniciar OBS]**

**[COMPU 2: Ejecutar]**
```sql
SELECT id, empleado, estado, dias_solicitados FROM permisos ORDER BY id;
```

**[COMPU 1: Crear permiso]**

**[COMPU 2: Repetir consulta]**
```sql
SELECT id, empleado, estado, dias_solicitados FROM permisos ORDER BY id;
```

---

## 🎬 RESULTADO ESPERADO

Al final del video habrás demostrado:
- ✅ 3 capas físicamente separadas
- ✅ Frontend interactivo
- ✅ Backend procesando solicitudes
- ✅ PostgreSQL guardando datos en tiempo real
- ✅ Sincronización entre capas
- ✅ Arquitectura escalable

---

## 📞 Comandos de Emergencia Durante el Video

Si algo falla:

```bash
# Reiniciar backend
docker compose restart backend

# Reiniciar frontend  
docker compose restart frontend

# Verificar logs
docker compose logs backend
```

---

¡Buena suerte con tu video! 🎥🚀

