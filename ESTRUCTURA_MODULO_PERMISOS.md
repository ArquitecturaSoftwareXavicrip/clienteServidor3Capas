# 🏗️ Estructura del Módulo de Permisos

## 📂 Árbol de Archivos

```
clienteServidor3Capas/
│
├── 📁 backend/                          # Tier 2 y 3: Backend
│   └── app/
│       ├── __init__.py                  # ✏️ MODIFICADO - Registrar permiso_bp
│       │
│       ├── 📁 models/                   # Tier 3: Modelos de Datos
│       │   ├── __init__.py              # ✏️ MODIFICADO - Importar Permiso
│       │   ├── empresa.py
│       │   ├── servicio.py
│       │   ├── contrato.py
│       │   └── permiso.py               # ✅ NUEVO - Modelo Permiso
│       │
│       ├── 📁 repositories/             # Tier 3: Acceso a Datos
│       │   ├── __init__.py
│       │   ├── empresa_repository.py
│       │   ├── servicio_repository.py
│       │   ├── contrato_repository.py
│       │   └── permiso_repository.py    # ✅ NUEVO - Repositorio Permiso
│       │
│       ├── 📁 services/                 # Tier 2: Lógica de Negocio
│       │   ├── __init__.py
│       │   ├── empresa_service.py
│       │   ├── servicio_service.py
│       │   ├── contrato_service.py
│       │   └── permiso_service.py       # ✅ NUEVO - Servicio Permiso
│       │
│       └── 📁 controllers/              # Tier 2: Controladores API
│           ├── __init__.py
│           ├── empresa_controller.py
│           ├── servicio_controller.py
│           ├── contrato_controller.py
│           └── permiso_controller.py    # ✅ NUEVO - Controlador Permiso
│
├── 📁 frontend/                         # Tier 1: Presentación
│   └── src/
│       ├── App.js                       # ✏️ MODIFICADO - Navegación Permisos
│       ├── App.css                      # ✏️ MODIFICADO - Estilos estados
│       │
│       ├── 📁 views/                    # Vistas React
│       │   ├── EmpresaView.js
│       │   ├── ServicioView.js
│       │   ├── ContratoView.js
│       │   └── PermisoView.js           # ✅ NUEVO - Vista Permisos
│       │
│       └── 📁 services/
│           └── api.js                   # ✏️ MODIFICADO - permisosAPI
│
├── 📁 database/
│   ├── schema.sql                       # ✏️ MODIFICADO - Tabla permisos
│   ├── init_db.py
│   └── init_permisos.py                 # ✅ NUEVO - Datos de ejemplo
│
├── 📁 Documentación/
│   ├── README.md                        # ✏️ MODIFICADO - Info módulo
│   ├── MODULO_PERMISOS.md              # ✅ NUEVO - Docs completa
│   ├── IMPLEMENTACION_PERMISOS.md      # ✅ NUEVO - Guía implementación
│   └── ESTRUCTURA_MODULO_PERMISOS.md   # ✅ NUEVO - Este archivo
│
└── docker-compose.yml

```

## 🎯 Resumen de Cambios

### ✅ Archivos Nuevos (10)

#### Backend (4 archivos)
1. `backend/app/models/permiso.py`
2. `backend/app/repositories/permiso_repository.py`
3. `backend/app/services/permiso_service.py`
4. `backend/app/controllers/permiso_controller.py`

#### Frontend (1 archivo)
5. `frontend/src/views/PermisoView.js`

#### Base de Datos (1 archivo)
6. `database/init_permisos.py`

#### Documentación (4 archivos)
7. `MODULO_PERMISOS.md`
8. `IMPLEMENTACION_PERMISOS.md`
9. `ESTRUCTURA_MODULO_PERMISOS.md`
10. (README.md modificado, no cuenta como nuevo)

### ✏️ Archivos Modificados (6)

1. `backend/app/__init__.py` - Registrar blueprint
2. `backend/app/models/__init__.py` - Importar modelo
3. `frontend/src/App.js` - Navegación y renderizado
4. `frontend/src/App.css` - Estilos de estados
5. `frontend/src/services/api.js` - API de permisos
6. `database/schema.sql` - Tabla de permisos
7. `README.md` - Documentación general

## 🔄 Flujo de Datos

```
┌─────────────────────────────────────────────────────────────┐
│                     FLUJO DE DATOS                          │
└─────────────────────────────────────────────────────────────┘

1️⃣ CREAR PERMISO
   Usuario → PermisoView (Formulario)
         ↓
   permisosAPI.create(data)
         ↓
   POST /api/permisos
         ↓
   permiso_controller.create_permiso()
         ↓
   PermisoService.create_permiso() [Validaciones]
         ↓
   PermisoRepository.create()
         ↓
   Permiso.to_dict() → Base de Datos
         ↓
   Respuesta JSON ← Usuario ve confirmación


2️⃣ LISTAR PERMISOS
   Usuario → PermisoView (componentDidMount)
         ↓
   permisosAPI.getAll()
         ↓
   GET /api/permisos
         ↓
   permiso_controller.get_all_permisos()
         ↓
   PermisoService.get_all_permisos()
         ↓
   PermisoRepository.get_all()
         ↓
   Base de Datos → [Permiso.to_dict() for p in permisos]
         ↓
   Array JSON ← Usuario ve tabla


3️⃣ APROBAR PERMISO
   Usuario → Click "Aprobar" → Confirmación
         ↓
   permisosAPI.aprobar(id)
         ↓
   POST /api/permisos/:id/aprobar
         ↓
   permiso_controller.aprobar_permiso()
         ↓
   PermisoService.aprobar_permiso()
         ↓
   PermisoRepository.update(id, {estado: 'aprobado'})
         ↓
   Base de Datos actualizada
         ↓
   Respuesta JSON ← Usuario ve estado actualizado


4️⃣ FILTRAR POR ESTADO
   Usuario → Selector de estado (ej: "Pendientes")
         ↓
   permisosAPI.getByEstado('pendiente')
         ↓
   GET /api/permisos?estado=pendiente
         ↓
   permiso_controller.get_all_permisos() [con query param]
         ↓
   PermisoService.get_permisos_by_estado('pendiente')
         ↓
   PermisoRepository.get_by_estado('pendiente')
         ↓
   Base de Datos → Filtrado
         ↓
   Array JSON ← Usuario ve solo pendientes
```

## 🧩 Componentes del Módulo

### 1. Modelo (Tier 3)

```python
# backend/app/models/permiso.py
class Permiso(db.Model):
    - id
    - empleado
    - tipo
    - fecha_inicio
    - fecha_fin
    - dias_solicitados
    - estado
    - observaciones
    
    Métodos:
    - to_dict()
    - __repr__()
```

### 2. Repositorio (Tier 3)

```python
# backend/app/repositories/permiso_repository.py
class PermisoRepository:
    - get_all()
    - get_by_id(id)
    - get_by_estado(estado)
    - create(data)
    - update(id, data)
    - delete(id)
```

### 3. Servicio (Tier 2)

```python
# backend/app/services/permiso_service.py
class PermisoService:
    - get_all_permisos()
    - get_permiso_by_id(id)
    - get_permisos_by_estado(estado)
    - create_permiso(data)          # ✅ Con validaciones
    - update_permiso(id, data)      # ✅ Con validaciones
    - delete_permiso(id)
    - aprobar_permiso(id, obs)      # ✅ Función especial
    - rechazar_permiso(id, obs)     # ✅ Función especial
```

### 4. Controlador (Tier 2)

```python
# backend/app/controllers/permiso_controller.py
Blueprint: permiso_bp (/api/permisos)

Endpoints:
- GET    /api/permisos              # Lista todos
- GET    /api/permisos?estado=X     # Filtra por estado
- GET    /api/permisos/:id          # Obtiene uno
- POST   /api/permisos              # Crea nuevo
- PUT    /api/permisos/:id          # Actualiza
- DELETE /api/permisos/:id          # Elimina
- POST   /api/permisos/:id/aprobar  # Aprueba
- POST   /api/permisos/:id/rechazar # Rechaza
```

### 5. Vista (Tier 1)

```javascript
// frontend/src/views/PermisoView.js
Componente React:

Estados:
- permisos[]
- loading
- error
- success
- editingId
- filtroEstado
- formData{}

Funciones:
- loadPermisos()
- handleSubmit()
- handleEdit()
- handleDelete()
- handleAprobar()
- handleRechazar()
- resetForm()

UI:
- Formulario de creación/edición
- Selector de filtro por estado
- Tabla con todos los permisos
- Botones de acción contextual
```

### 6. API Client (Tier 1)

```javascript
// frontend/src/services/api.js
export const permisosAPI = {
    getAll: () => GET /permisos
    getById: (id) => GET /permisos/:id
    getByEstado: (estado) => GET /permisos?estado=:estado
    create: (data) => POST /permisos
    update: (id, data) => PUT /permisos/:id
    delete: (id) => DELETE /permisos/:id
    aprobar: (id, obs) => POST /permisos/:id/aprobar
    rechazar: (id, obs) => POST /permisos/:id/rechazar
}
```

## 🎨 Interfaz de Usuario

```
┌─────────────────────────────────────────────────────────┐
│  Servicios de Limpieza para Empresas                   │
│  ┌──────┬──────────┬──────────┬────────────┐          │
│  │Empresas│Servicios│Contratos│[Permisos]◄─┘          │
│  └──────┴──────────┴──────────┴────────────┘          │
└─────────────────────────────────────────────────────────┘

┌───────────────────────────────────────────────────────────┐
│  📝 Nuevo Permiso de Vacaciones                          │
│  ┌─────────────────────────────────────────────────────┐ │
│  │ Empleado: [___________________________________]     │ │
│  │ Tipo: [Vacaciones] (readonly)                      │ │
│  │ Fecha Inicio: [📅 YYYY-MM-DD]                      │ │
│  │ Fecha Fin: [📅 YYYY-MM-DD]                         │ │
│  │ Días Solicitados: [____]                           │ │
│  │ Observaciones: [________________________________]  │ │
│  │                [________________________________]  │ │
│  │  [Crear] [Cancelar]                                │ │
│  └─────────────────────────────────────────────────────┘ │
└───────────────────────────────────────────────────────────┘

┌───────────────────────────────────────────────────────────┐
│  📋 Lista de Permisos de Vacaciones                      │
│  Filtrar por estado: [ Todos ▼]                          │
│  ┌─────────────────────────────────────────────────────┐ │
│  │ID│Empleado│Tipo│F.Inicio│F.Fin│Días│Estado│Acciones│ │
│  ├──┼────────┼────┼────────┼─────┼────┼──────┼────────┤ │
│  │1 │Juan P. │Vac.│2024... │...  │ 7  │🟡PEND│[Aprobar]│ │
│  │  │        │    │        │     │    │      │[Rechazar]│ │
│  │  │        │    │        │     │    │      │[Editar] │ │
│  │  │        │    │        │     │    │      │[Eliminar]│ │
│  ├──┼────────┼────┼────────┼─────┼────┼──────┼────────┤ │
│  │2 │María G.│Vac.│2024... │...  │14  │🟢APRO│[Editar] │ │
│  │  │        │    │        │     │    │      │[Eliminar]│ │
│  ├──┼────────┼────┼────────┼─────┼────┼──────┼────────┤ │
│  │3 │Carlos R│Vac.│2024... │...  │ 5  │🔴RECH│[Editar] │ │
│  │  │        │    │        │     │    │      │[Eliminar]│ │
│  └─────────────────────────────────────────────────────┘ │
└───────────────────────────────────────────────────────────┘
```

## 📊 Diagrama de Capas

```
┌────────────────────────────────────────────────────────────┐
│                    TIER 1: PRESENTACIÓN                    │
│  ┌──────────────────────────────────────────────────────┐  │
│  │             PermisoView.js (React)                   │  │
│  │  - Formulario CRUD                                   │  │
│  │  - Tabla de permisos                                 │  │
│  │  - Filtros y acciones                                │  │
│  └────────────────────┬─────────────────────────────────┘  │
│                       │ HTTP/REST (permisosAPI)            │
└───────────────────────┼────────────────────────────────────┘
                        │
┌───────────────────────▼────────────────────────────────────┐
│              TIER 2: LÓGICA DE NEGOCIO                     │
│  ┌──────────────────────────────────────────────────────┐  │
│  │     permiso_controller.py (Flask Blueprint)          │  │
│  │  - GET /api/permisos                                 │  │
│  │  - POST /api/permisos                                │  │
│  │  - PUT /api/permisos/:id                             │  │
│  │  - POST /api/permisos/:id/aprobar                    │  │
│  └────────────────────┬─────────────────────────────────┘  │
│                       │                                    │
│  ┌────────────────────▼─────────────────────────────────┐  │
│  │         PermisoService (Lógica de Negocio)           │  │
│  │  - Validaciones                                      │  │
│  │  - Reglas de negocio                                 │  │
│  │  - Transformaciones                                  │  │
│  └────────────────────┬─────────────────────────────────┘  │
└───────────────────────┼────────────────────────────────────┘
                        │
┌───────────────────────▼────────────────────────────────────┐
│              TIER 3: ACCESO A DATOS                        │
│  ┌──────────────────────────────────────────────────────┐  │
│  │       PermisoRepository (Data Access)                │  │
│  │  - CRUD operations                                   │  │
│  │  - Queries específicos                               │  │
│  └────────────────────┬─────────────────────────────────┘  │
│                       │                                    │
│  ┌────────────────────▼─────────────────────────────────┐  │
│  │         Permiso Model (SQLAlchemy ORM)               │  │
│  │  - Mapeo objeto-relacional                           │  │
│  │  - Definición de schema                              │  │
│  └────────────────────┬─────────────────────────────────┘  │
│                       │ SQL                                │
│  ┌────────────────────▼─────────────────────────────────┐  │
│  │              Base de Datos (SQLite)                  │  │
│  │  - Tabla: permisos                                   │  │
│  └──────────────────────────────────────────────────────┘  │
└────────────────────────────────────────────────────────────┘
```

## ✅ Checklist de Implementación

### Backend
- [x] Modelo Permiso creado
- [x] Repositorio con CRUD completo
- [x] Servicio con validaciones
- [x] Controlador con 8 endpoints
- [x] Blueprint registrado en app
- [x] Modelo importado en __init__

### Frontend
- [x] Vista React creada
- [x] Formulario de creación/edición
- [x] Tabla de visualización
- [x] Filtro por estado
- [x] Botones de acción
- [x] API client configurado
- [x] Navegación agregada en App.js
- [x] Estilos CSS agregados

### Base de Datos
- [x] Schema actualizado
- [x] Script de datos de ejemplo

### Documentación
- [x] README actualizado
- [x] Documentación técnica completa
- [x] Guía de implementación
- [x] Estructura documentada

## 🎉 ¡Todo Listo!

El módulo está **100% completo** y funcional. Sigue las instrucciones en `IMPLEMENTACION_PERMISOS.md` para probarlo.

