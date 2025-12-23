# Módulo de Permisos (Vacaciones)

## 📋 Descripción

Este módulo permite gestionar solicitudes de permisos de vacaciones para empleados, incluyendo la creación, aprobación, rechazo y seguimiento de solicitudes.

## 🏗️ Arquitectura

El módulo sigue la arquitectura de 3 capas del proyecto:

### Tier 3: Acceso a Datos (Backend)
- **Modelo**: `backend/app/models/permiso.py`
- **Repositorio**: `backend/app/repositories/permiso_repository.py`

### Tier 2: Lógica de Negocio (Backend)
- **Servicio**: `backend/app/services/permiso_service.py`
- **Controlador**: `backend/app/controllers/permiso_controller.py`

### Tier 1: Presentación (Frontend)
- **Vista**: `frontend/src/views/PermisoView.js`
- **API Client**: `frontend/src/services/api.js` (permisosAPI)

## 📊 Base de Datos

### Tabla: permisos

| Campo | Tipo | Descripción |
|-------|------|-------------|
| id | INTEGER | Identificador único (PK) |
| empleado | VARCHAR(100) | Nombre completo del empleado |
| tipo | VARCHAR(50) | Tipo de permiso (por defecto: "Vacaciones") |
| fecha_inicio | DATE | Fecha de inicio del permiso |
| fecha_fin | DATE | Fecha de finalización del permiso |
| dias_solicitados | INTEGER | Número de días solicitados |
| estado | VARCHAR(20) | Estado del permiso (pendiente, aprobado, rechazado) |
| observaciones | TEXT | Notas u observaciones adicionales |

## 🔌 API Endpoints

### GET /api/permisos
Obtiene todos los permisos o filtra por estado.

**Query Parameters:**
- `estado` (opcional): pendiente, aprobado, rechazado

**Respuesta exitosa (200):**
```json
[
  {
    "id": 1,
    "empleado": "Juan Pérez",
    "tipo": "Vacaciones",
    "fecha_inicio": "2024-01-15",
    "fecha_fin": "2024-01-20",
    "dias_solicitados": 5,
    "estado": "pendiente",
    "observaciones": "Vacaciones de verano"
  }
]
```

### GET /api/permisos/:id
Obtiene un permiso específico por ID.

**Respuesta exitosa (200):**
```json
{
  "id": 1,
  "empleado": "Juan Pérez",
  "tipo": "Vacaciones",
  "fecha_inicio": "2024-01-15",
  "fecha_fin": "2024-01-20",
  "dias_solicitados": 5,
  "estado": "pendiente",
  "observaciones": "Vacaciones de verano"
}
```

### POST /api/permisos
Crea un nuevo permiso.

**Request Body:**
```json
{
  "empleado": "Juan Pérez",
  "tipo": "Vacaciones",
  "fecha_inicio": "2024-01-15",
  "fecha_fin": "2024-01-20",
  "dias_solicitados": 5,
  "observaciones": "Vacaciones de verano"
}
```

**Respuesta exitosa (201):**
```json
{
  "id": 1,
  "empleado": "Juan Pérez",
  "tipo": "Vacaciones",
  "fecha_inicio": "2024-01-15",
  "fecha_fin": "2024-01-20",
  "dias_solicitados": 5,
  "estado": "pendiente",
  "observaciones": "Vacaciones de verano"
}
```

### PUT /api/permisos/:id
Actualiza un permiso existente.

**Request Body:**
```json
{
  "empleado": "Juan Pérez Actualizado",
  "fecha_inicio": "2024-01-16",
  "fecha_fin": "2024-01-21",
  "dias_solicitados": 5,
  "estado": "aprobado",
  "observaciones": "Aprobado por gerencia"
}
```

### DELETE /api/permisos/:id
Elimina un permiso.

**Respuesta exitosa (200):**
```json
{
  "message": "Permiso eliminado correctamente"
}
```

### POST /api/permisos/:id/aprobar
Aprueba un permiso.

**Request Body (opcional):**
```json
{
  "observaciones": "Aprobado por gerencia"
}
```

**Respuesta exitosa (200):**
```json
{
  "id": 1,
  "empleado": "Juan Pérez",
  "tipo": "Vacaciones",
  "fecha_inicio": "2024-01-15",
  "fecha_fin": "2024-01-20",
  "dias_solicitados": 5,
  "estado": "aprobado",
  "observaciones": "Aprobado por gerencia"
}
```

### POST /api/permisos/:id/rechazar
Rechaza un permiso.

**Request Body (opcional):**
```json
{
  "observaciones": "No hay cobertura disponible"
}
```

## 🎨 Interfaz de Usuario

### Formulario de Creación/Edición
- Empleado (texto requerido)
- Tipo (fijo: "Vacaciones")
- Fecha de Inicio (date picker requerido)
- Fecha de Fin (date picker requerido)
- Días Solicitados (número requerido, mínimo 1)
- Estado (select - solo en edición)
- Observaciones (textarea opcional)

### Tabla de Permisos
Muestra todos los permisos con:
- ID
- Empleado
- Tipo
- Fecha Inicio
- Fecha Fin
- Días Solicitados
- Estado (con badge de color)
- Observaciones
- Acciones (Aprobar, Rechazar, Editar, Eliminar)

### Filtro por Estado
Permite filtrar los permisos por:
- Todos
- Pendientes
- Aprobados
- Rechazados

## ✅ Validaciones

### Backend (Capa de Servicio)

1. **Empleado**: Requerido, no puede estar vacío
2. **Fecha de Inicio**: Requerida, formato YYYY-MM-DD
3. **Fecha de Fin**: Requerida, formato YYYY-MM-DD, debe ser posterior a fecha de inicio
4. **Días Solicitados**: Requerido, debe ser mayor a 0, no puede exceder el rango de fechas
5. **Estado**: Debe ser uno de: pendiente, aprobado, rechazado
6. **Email**: Debe contener @ (si se agrega en futuras versiones)

### Frontend

1. Validación de campos requeridos (HTML5)
2. Tipo de dato numérico para días
3. Tipo de dato fecha para fechas
4. Confirmación antes de eliminar

## 🚀 Cómo Usar

### 1. Ejecutar la Aplicación

```bash
# Con Docker (recomendado)
docker compose up --build

# O manualmente
# Terminal 1 - Backend
cd backend
source venv/bin/activate  # o .\venv\Scripts\Activate.ps1 en Windows
python run.py

# Terminal 2 - Frontend
cd frontend
npm start
```

### 2. Acceder al Módulo

1. Abrir navegador en `http://localhost:3001`
2. Hacer clic en el botón "Permisos" en la navegación
3. Se mostrará la vista de gestión de permisos

### 3. Crear un Permiso

1. Completar el formulario con:
   - Nombre del empleado
   - Fecha de inicio
   - Fecha de fin
   - Días solicitados
   - Observaciones (opcional)
2. Hacer clic en "Crear"

### 4. Aprobar/Rechazar Permisos

- Los permisos en estado "pendiente" muestran botones de Aprobar y Rechazar
- Al hacer clic en "Rechazar", se puede agregar un motivo
- El estado cambiará automáticamente y se mostrará con un badge de color

### 5. Filtrar Permisos

- Usar el selector "Filtrar por estado" encima de la tabla
- Seleccionar: Todos, Pendientes, Aprobados o Rechazados

## 🎨 Estilos de Estados

Los estados se muestran con badges de colores:
- **Pendiente**: Amarillo (warning)
- **Aprobado**: Verde (success)
- **Rechazado**: Rojo (danger)

## 🔧 Extensiones Futuras

Posibles mejoras al módulo:

1. **Calendario Visual**: Integrar un calendario para visualizar permisos
2. **Notificaciones**: Enviar emails cuando se apruebe/rechace un permiso
3. **Historial**: Mantener un historial de cambios de estado
4. **Conflictos**: Detectar si múltiples empleados solicitan el mismo período
5. **Tipos de Permiso**: Agregar otros tipos (enfermedad, personal, etc.)
6. **Roles de Usuario**: Diferentes permisos según rol (empleado vs. manager)
7. **Reportes**: Generar reportes de permisos por período
8. **Balance de Días**: Llevar control de días de vacaciones disponibles por empleado

## 📝 Notas Técnicas

- El módulo sigue el mismo patrón que los módulos existentes (Empresas, Servicios, Contratos)
- Usa SQLAlchemy ORM para la persistencia de datos
- Implementa validaciones tanto en backend (Python) como frontend (React)
- Los endpoints REST siguen las convenciones RESTful
- Las fechas se manejan en formato ISO (YYYY-MM-DD)
- El estado por defecto de un nuevo permiso es "pendiente"

## 🐛 Troubleshooting

### Error: "Permiso no encontrado"
- Verificar que el ID del permiso existe en la base de datos
- Recargar la lista de permisos

### Error: "La fecha de fin debe ser posterior a la fecha de inicio"
- Verificar que la fecha de fin sea mayor a la fecha de inicio
- Verificar que los días solicitados sean coherentes con el rango de fechas

### Error: "Los días solicitados no pueden ser mayores al rango de fechas"
- Calcular correctamente los días entre fecha_inicio y fecha_fin
- Ajustar el campo dias_solicitados

## 📚 Recursos

- [Documentación del Proyecto](README.md)
- [Guía de Arquitectura](ARQUITECTURA.md)
- [Guía del Estudiante](GuiaEstudiante.md)

---

**Desarrollado siguiendo la arquitectura de 3 capas del proyecto** 🏗️

