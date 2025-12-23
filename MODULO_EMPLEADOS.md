# 📋 Módulo de Empleados

## 🎯 Descripción

El módulo de **Empleados** gestiona el personal de la empresa de limpieza, permitiendo registrar, actualizar y consultar información de los empleados.

## 🏗️ Arquitectura de 3 Capas

### Tier 3: Acceso a Datos
- **Modelo**: `backend/app/models/empleado.py`
- **Repositorio**: `backend/app/repositories/empleado_repository.py`

### Tier 2: Lógica de Negocio
- **Servicio**: `backend/app/services/empleado_service.py`
- **Controlador**: `backend/app/controllers/empleado_controller.py`

### Tier 1: Presentación
- **Vista**: `frontend/src/views/EmpleadoView.js`
- **API Client**: `frontend/src/services/api.js` (empleadosAPI)

## 📊 Estructura de Datos

### Tabla: empleados

| Campo | Tipo | Descripción |
|-------|------|-------------|
| id | SERIAL | Identificador único (PK) |
| nombre | VARCHAR(100) | Nombre del empleado |
| apellido | VARCHAR(100) | Apellido del empleado |
| email | VARCHAR(100) | Correo electrónico |
| telefono | VARCHAR(20) | Teléfono de contacto |
| cargo | VARCHAR(50) | Cargo o posición |

## 🔌 API Endpoints

### GET /api/empleados
Obtiene todos los empleados.

**Respuesta exitosa (200):**
```json
[
  {
    "id": 1,
    "nombre": "Juan",
    "apellido": "Pérez García",
    "email": "juan.perez@limpieza.com",
    "telefono": "0991234567",
    "cargo": "Gerente General"
  }
]
```

### GET /api/empleados/:id
Obtiene un empleado específico por ID.

### POST /api/empleados
Crea un nuevo empleado.

**Request Body:**
```json
{
  "nombre": "Juan",
  "apellido": "Pérez García",
  "email": "juan.perez@limpieza.com",
  "telefono": "0991234567",
  "cargo": "Gerente General"
}
```

### PUT /api/empleados/:id
Actualiza un empleado existente.

### DELETE /api/empleados/:id
Elimina un empleado.

## ✅ Validaciones

### Backend
- Nombre: requerido, no vacío
- Apellido: requerido, no vacío
- Email: requerido, formato válido (@)
- Teléfono: requerido
- Cargo: requerido

### Frontend
- Validación HTML5 de campos requeridos
- Validación de formato de email

## 🎨 Interfaz de Usuario

### Formulario
- Nombre (texto)
- Apellido (texto)
- Email (email)
- Teléfono (texto)
- Cargo (texto con placeholder de ejemplos)

### Tabla
Muestra todos los empleados con columnas:
- ID
- Nombre
- Apellido
- Email
- Teléfono
- Cargo
- Acciones (Editar, Eliminar)

## 🚀 Cómo Usar

### 1. Crear Tablas

```bash
# PostgreSQL
psql -U postgres -d limpieza_empresas -f database/schema.sql
```

### 2. Cargar Datos de Ejemplo

```bash
cd database
python init_empleados.py
```

### 3. Acceder al Módulo

1. Abrir http://localhost:3001
2. Hacer clic en "Empleados"
3. Ver 8 empleados de ejemplo
4. Crear, editar o eliminar empleados

## 📚 Datos de Ejemplo

El script `init_empleados.py` crea 8 empleados:

| Nombre | Cargo |
|--------|-------|
| Juan Pérez García | Gerente General |
| María González López | Supervisor de Limpieza |
| Carlos Rodríguez Sánchez | Operario de Limpieza |
| Ana Martínez Torres | Operario de Limpieza |
| Luis Fernández Ruiz | Supervisor de Área |
| Carmen López Díaz | Coordinador Administrativo |
| Pedro Sánchez Morales | Operario de Limpieza |
| Laura Torres Vega | Jefe de Recursos Humanos |

## 🎓 Aprendizajes

Este módulo demuestra:
- ✅ Arquitectura de 3 capas
- ✅ Patrón MVC completo
- ✅ CRUD completo
- ✅ Validaciones en múltiples capas
- ✅ API RESTful
- ✅ Integración Frontend-Backend

---

**Desarrollado siguiendo la GuiaEstudiante.md** 📚

