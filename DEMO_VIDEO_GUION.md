# 🎬 GUIÓN COMPLETO PARA VIDEO - Demo Arquitectura 3 Capas

## 🎯 Configuración Recomendada para el Video

### Setup Más Fácil: 1 Servidor + 1 Cliente

**COMPUTADORA 1 (Servidor):**
- Backend + PostgreSQL en Docker
- IP: Obtener con `ipconfig` (ej: 192.168.1.20)
- Sistema: Windows con Docker Desktop

**COMPUTADORA 2 (Cliente):**  
- Solo navegador web
- Accede al frontend del servidor
- Puede ser tu laptop, celular, o tablet

---

## ⚡ SETUP EN 5 MINUTOS

### COMPU 1 (Servidor) - Antes de Grabar

```powershell
# 1. Iniciar Docker
docker compose up --build -d

# 2. Esperar y cargar datos
Start-Sleep -Seconds 15
docker exec limpieza_backend python ../database/init_db.py
docker exec limpieza_backend python ../database/init_permisos.py
docker exec limpieza_backend python ../database/init_empleados.py

# 3. Obtener tu IP
ipconfig
# Buscar "Dirección IPv4" de tu red WiFi/Ethernet
# Ejemplo: 192.168.1.20

# 4. Abrir terminal de PostgreSQL
docker exec -it limpieza_db psql -U postgres -d limpieza_empresas
```

### COMPU 2 (Cliente) - Antes de Grabar

```
Abrir navegador en:
http://192.168.1.20:3001

(Usar la IP real de COMPU 1)
```

---

## 🎬 GUIÓN DEL VIDEO (6 MINUTOS)

### 📺 ESCENA 1: Intro (0:00 - 0:30)

**[Visual: Diagrama en PowerPoint o papel]**

**Narración:**
> "Hola, hoy voy a demostrar una arquitectura de 3 capas Cliente-Servidor con separación física de componentes."
>
> "Tengo dos computadoras: esta [mostrar COMPU 1] tiene el backend y la base de datos PostgreSQL, y esta otra [mostrar COMPU 2] va a acceder al frontend como cliente."

---

### 📺 ESCENA 2: Mostrar Estado Inicial BD (0:30 - 1:00)

**[Visual: COMPU 1 - Terminal PostgreSQL]**

**Comandos a ejecutar:**
```sql
-- Mostrar que estás conectado
SELECT current_database();

-- Contar permisos actuales
SELECT COUNT(*) as total_permisos FROM permisos;

-- Mostrar los permisos existentes
SELECT id, empleado, estado, dias_solicitados 
FROM permisos 
ORDER BY id;
```

**Narración:**
> "Aquí en el servidor tengo PostgreSQL con la base de datos 'limpieza_empresas'."
>
> "Actualmente tengo 6 permisos de vacaciones registrados. Voy a crear uno nuevo desde la otra computadora y vamos a verlo aparecer aquí en tiempo real."

---

### 📺 ESCENA 3: Crear Permiso desde Cliente (1:00 - 2:30)

**[Visual: COMPU 2 - Navegador]**

**Mostrar la URL en la barra:**
```
http://192.168.1.20:3001
```

**Narración:**
> "Desde la otra computadora, accedo al frontend usando la IP del servidor."

**Acciones:**
1. Mostrar la aplicación cargada
2. Clic en "Permisos"
3. Mostrar la tabla con 6 permisos

**Narración:**
> "Aquí veo la misma información que está en la base de datos."
>
> "Ahora voy a crear una nueva solicitud de vacaciones."

**[Llenar formulario:]**
```
Empleado: [Tu Nombre]
Tipo: Vacaciones
Fecha Inicio: [Seleccionar 7 días adelante]
Fecha Fin: [Seleccionar 14 días adelante]
Días Solicitados: 7
Observaciones: Demo arquitectura 3 capas - Video en vivo
```

**[Hacer clic en "Crear"]**

**Narración:**
> "Al hacer clic en crear, esta solicitud viaja por la red desde mi laptop hasta el servidor, el backend procesa la petición, valida los datos, y la guarda en PostgreSQL."

**[Mostrar mensaje de éxito: "Permiso creado correctamente"]**

**[Mostrar que aparece en la tabla con estado PENDIENTE 🟡]**

---

### 📺 ESCENA 4: Verificar en Base de Datos (2:30 - 3:15)

**[Visual: COMPU 1 - Terminal PostgreSQL - Split screen con COMPU 2]**

**Comandos:**
```sql
-- Contar nuevamente
SELECT COUNT(*) FROM permisos;
-- Ahora muestra 7

-- Ver el nuevo permiso
SELECT * FROM permisos ORDER BY id DESC LIMIT 1;

-- O con formato bonito:
SELECT 
    id,
    empleado,
    estado,
    fecha_inicio,
    fecha_fin,
    dias_solicitados,
    observaciones
FROM permisos 
WHERE id = (SELECT MAX(id) FROM permisos);
```

**Narración:**
> "¡Y aquí está! El permiso se guardó instantáneamente en la base de datos."
>
> "Como pueden ver, ahora tenemos 7 permisos en lugar de 6."
>
> "Este es el registro que acabo de crear desde la otra computadora: [leer datos]"

---

### 📺 ESCENA 5: Aprobar Permiso (3:15 - 4:00)

**[Visual: COMPU 2 - Navegador]**

**Narración:**
> "Ahora voy a aprobar este permiso desde el frontend."

**[Buscar el permiso recién creado]**

**[Hacer clic en botón "Aprobar"]**

**[Confirmar en el diálogo]**

**[Mostrar que el badge cambia de 🟡 PENDIENTE a 🟢 APROBADO]**

**Narración:**
> "El estado cambió inmediatamente. Esto activó otra petición HTTP al backend que actualizó el registro en PostgreSQL."

---

### 📺 ESCENA 6: Verificar Aprobación en BD (4:00 - 4:30)

**[Visual: COMPU 1 - Terminal PostgreSQL]**

**Comandos:**
```sql
-- Ver el cambio de estado
SELECT id, empleado, estado 
FROM permisos 
WHERE empleado LIKE '%[Tu Nombre]%';

-- Ver todos los aprobados
SELECT id, empleado, estado 
FROM permisos 
WHERE estado = 'aprobado'
ORDER BY id;
```

**Narración:**
> "Y aquí vemos que el estado cambió a 'aprobado' en la base de datos."
>
> "Esta es la arquitectura de 3 capas en acción: Frontend, Backend y Base de Datos trabajando juntos pero en nodos separados."

---

### 📺 ESCENA 7: Demostrar Filtros (4:30 - 5:00)

**[Visual: COMPU 2 - Navegador]**

**Acciones:**
1. Usar el selector "Filtrar por estado"
2. Seleccionar "Aprobados"
3. Mostrar que solo aparecen los aprobados

**Narración:**
> "El sistema también permite filtrar. Cuando filtro por 'Aprobados', el frontend hace una petición al backend con el parámetro de filtro."

**[COMPU 1: Mostrar la consulta SQL equivalente]**

```sql
SELECT * FROM permisos WHERE estado = 'aprobado';
```

---

### 📺 ESCENA 8: Conclusión (5:00 - 6:00)

**[Visual: Volver al diagrama de arquitectura]**

**Narración:**
> "En resumen, hemos demostrado:"
>
> "✅ Tier 1 - Presentación: Frontend React accesible desde cualquier dispositivo"
>
> "✅ Tier 2 - Lógica de Negocio: Backend Flask procesando y validando solicitudes"
>
> "✅ Tier 3 - Datos: PostgreSQL almacenando información de forma persistente y segura"
>
> "Esta arquitectura permite:"
> "- Escalar cada capa independientemente"
> "- Desplegar en diferentes servidores"
> "- Mantener el código organizado y mantenible"
> "- Facilitar el trabajo en equipo"
>
> "Gracias por ver este video. El código está disponible en GitHub."

**[Mostrar: https://github.com/samuelanyoneai/clienteServidor3Capas]**

---

## 📊 VARIACIONES DEL DEMO

### Variación 1: También Mostrar Empleados

Después de mostrar permisos, crear un empleado:

```
Nombre: Pedro
Apellido: Sánchez
Email: pedro@empresa.com
Teléfono: 0991234567
Cargo: Supervisor
```

Verificar en BD:
```sql
SELECT * FROM empleados ORDER BY id DESC LIMIT 1;
```

### Variación 2: Mostrar Logs del Backend

```bash
# En COMPU 1, mostrar logs mientras se crea
docker compose logs -f backend

# Se verá:
# POST /api/permisos 201
```

---

## 🎥 EDICIÓN POST-GRABACIÓN

### Agregar en Edición:

1. **Títulos:**
   - "COMPU 1: Servidor (Backend + PostgreSQL)"
   - "COMPU 2: Cliente (Frontend)"

2. **Anotaciones:**
   - Flechas mostrando el flujo de datos
   - Resaltar IPs y puertos
   - Destacar el nuevo registro en verde

3. **Música de Fondo:**
   - Música suave que no interfiera con narración

4. **Transiciones:**
   - Suaves entre escenas
   - Destacar cambios importantes

---

## ✅ CHECKLIST FINAL

Antes de publicar el video, verificar:
- [ ] Audio claro y sin ruido
- [ ] Pantallas legibles (fuente grande)
- [ ] IPs y configuración visibles
- [ ] Cada paso está explicado
- [ ] Se ve el flujo de datos claramente
- [ ] Conclusión resume los puntos clave
- [ ] Link a GitHub al final

---

¡Éxito con tu video! 🎬✨

