# Nuevos Módulos: Empleados y Facturas

## Resumen de Cambios

Se han agregado dos nuevos módulos completos al proyecto siguiendo la arquitectura de 3 capas y el patrón MVC:

### 1. Módulo de Empleados

#### Backend (Tier 2 y 3)

**Archivos Creados:**
- `backend/app/models/empleado.py` - Modelo de dominio
- `backend/app/repositories/empleado_repository.py` - Capa de acceso a datos
- `backend/app/services/empleado_service.py` - Lógica de negocio
- `backend/app/controllers/empleado_controller.py` - Controlador MVC

**Archivos Modificados:**
- `backend/app/models/__init__.py` - Importación del modelo Empleado
- `backend/app/__init__.py` - Registro del blueprint empleado_bp

#### Frontend (Tier 1)

**Archivos Creados:**
- `frontend/src/views/EmpleadoView.js` - Vista React para gestión de empleados

**Archivos Modificados:**
- `frontend/src/services/api.js` - Agregado empleadosAPI
- `frontend/src/App.js` - Importación de EmpleadoView y botón de navegación

#### Campos del Modelo Empleado
- `id` (Integer, PK)
- `nombre` (String, 100, NOT NULL)
- `apellido` (String, 100, NOT NULL)
- `email` (String, 100, NOT NULL)
- `telefono` (String, 20, NOT NULL)
- `cargo` (String, 50, NOT NULL)

#### Validaciones Implementadas
- Nombre y apellido requeridos y no vacíos
- Email requerido y debe contener @
- Teléfono requerido y no vacío
- Cargo requerido y no vacío

#### Endpoints API
```
GET    /api/empleados              - Listar todos
GET    /api/empleados/<id>         - Obtener por ID
POST   /api/empleados              - Crear nuevo
PUT    /api/empleados/<id>         - Actualizar
DELETE /api/empleados/<id>         - Eliminar
```

---

### 2. Módulo de Facturas

#### Backend (Tier 2 y 3)

**Archivos Creados:**
- `backend/app/models/factura.py` - Modelo de dominio
- `backend/app/repositories/factura_repository.py` - Capa de acceso a datos
- `backend/app/services/factura_service.py` - Lógica de negocio
- `backend/app/controllers/factura_controller.py` - Controlador MVC

**Archivos Modificados:**
- `backend/app/models/__init__.py` - Importación del modelo Factura
- `backend/app/__init__.py` - Registro del blueprint factura_bp

#### Frontend (Tier 1)

**Archivos Creados:**
- `frontend/src/views/FacturaView.js` - Vista React para gestión de facturas

**Archivos Modificados:**
- `frontend/src/services/api.js` - Agregado facturasAPI
- `frontend/src/App.js` - Importación de FacturaView y botón de navegación

#### Campos del Modelo Factura
- `id` (Integer, PK)
- `empresa_id` (Integer, FK → empresas.id, NOT NULL)
- `empleado_id` (Integer, FK → empleados.id, NOT NULL)
- `servicio_id` (Integer, FK → servicios.id, NOT NULL)
- `fecha_factura` (Date, NOT NULL, default: hoy)
- `fecha_vencimiento` (Date, NOT NULL)
- `descripcion` (String, 500, NOT NULL)
- `cantidad` (Integer, NOT NULL)
- `precio_unitario` (Float, NOT NULL)
- `subtotal` (Float, NOT NULL, calculado automáticamente)
- `impuesto` (Float, default: 0.0)
- `total` (Float, NOT NULL, calculado automáticamente)
- `estado` (String, 20, default: 'pendiente')

#### Validaciones Implementadas
- Empresa, empleado y servicio deben existir en la BD
- Descripción requerida y no vacía
- Cantidad debe ser > 0
- Precio unitario debe ser válido (≥ 0)
- Fecha de vencimiento requerida
- Cálculo automático de subtotal y total

#### Cálculos Automáticos
- `subtotal = cantidad × precio_unitario`
- `total = subtotal + impuesto`

#### Endpoints API
```
GET    /api/facturas                    - Listar todas
GET    /api/facturas/<id>               - Obtener por ID
GET    /api/facturas/empresa/<empresa_id> - Obtener por empresa
POST   /api/facturas                    - Crear nueva
PUT    /api/facturas/<id>               - Actualizar
DELETE /api/facturas/<id>               - Eliminar
```

---

## Relaciones entre Módulos

```
┌─────────────┐
│  Empresa    │
└──────┬──────┘
       │ (1:N)
       │
    ┌──▼────────────┐
    │   Factura     │
    └──┬──────┬──┬──┘
       │      │  │
       │      │  └─── FK: servicio_id → Servicio
       │      └────── FK: empleado_id → Empleado
       └───────────── FK: empresa_id → Empresa

┌──────────────┐
│  Empleado    │
└──────┬───────┘
       │ (1:N)
       │
       └─────────────► Factura
```

---

## Cómo Usar los Nuevos Módulos

### Crear un Empleado

**Frontend**: Navega a la pestaña "Empleados" y completa el formulario con:
- Nombre
- Apellido
- Email
- Teléfono
- Cargo

**API**:
```bash
curl -X POST http://localhost:5001/api/empleados \
  -H "Content-Type: application/json" \
  -d '{
    "nombre": "Juan",
    "apellido": "Pérez",
    "email": "juan@example.com",
    "telefono": "555-1234",
    "cargo": "Supervisor"
  }'
```

### Crear una Factura

**Frontend**: Navega a la pestaña "Facturas" y completa el formulario con:
- Empresa (dropdown)
- Empleado (dropdown)
- Servicio (dropdown)
- Fecha de Factura
- Fecha de Vencimiento
- Descripción
- Cantidad
- Precio Unitario
- Impuesto (opcional)
- Estado

**API**:
```bash
curl -X POST http://localhost:5001/api/facturas \
  -H "Content-Type: application/json" \
  -d '{
    "empresa_id": 1,
    "empleado_id": 1,
    "servicio_id": 1,
    "fecha_factura": "2024-01-15",
    "fecha_vencimiento": "2024-02-15",
    "descripcion": "Servicio de limpieza profunda",
    "cantidad": 5,
    "precio_unitario": 100.00,
    "impuesto": 50.00,
    "estado": "pendiente"
  }'
```

---

## Estructura de Archivos Actualizada

```
backend/
├── app/
│   ├── models/
│   │   ├── __init__.py (ACTUALIZADO)
│   │   ├── empresa.py
│   │   ├── servicio.py
│   │   ├── contrato.py
│   │   ├── empleado.py (NUEVO)
│   │   └── factura.py (NUEVO)
│   ├── repositories/
│   │   ├── empresa_repository.py
│   │   ├── servicio_repository.py
│   │   ├── contrato_repository.py
│   │   ├── empleado_repository.py (NUEVO)
│   │   └── factura_repository.py (NUEVO)
│   ├── services/
│   │   ├── empresa_service.py
│   │   ├── servicio_service.py
│   │   ├── contrato_service.py
│   │   ├── empleado_service.py (NUEVO)
│   │   └── factura_service.py (NUEVO)
│   ├── controllers/
│   │   ├── empresa_controller.py
│   │   ├── servicio_controller.py
│   │   ├── contrato_controller.py
│   │   ├── empleado_controller.py (NUEVO)
│   │   └── factura_controller.py (NUEVO)
│   └── __init__.py (ACTUALIZADO)

frontend/
├── src/
│   ├── views/
│   │   ├── EmpresaView.js
│   │   ├── ServicioView.js
│   │   ├── ContratoView.js
│   │   ├── EmpleadoView.js (NUEVO)
│   │   └── FacturaView.js (NUEVO)
│   ├── services/
│   │   └── api.js (ACTUALIZADO)
│   └── App.js (ACTUALIZADO)
```

---

## Pruebas Recomendadas

1. **Crear Empleados**:
   - Crear un empleado con datos válidos
   - Intentar crear sin nombre (debe fallar)
   - Intentar crear con email inválido (debe fallar)

2. **Crear Facturas**:
   - Crear una factura seleccionando empresa, empleado y servicio existentes
   - Verificar que los totales se calculan correctamente
   - Intentar crear sin empresa (debe fallar)
   - Intentar crear con cantidad negativa (debe fallar)

3. **Editar y Eliminar**:
   - Editar un empleado y verificar cambios
   - Editar una factura y verificar recálculo de totales
   - Eliminar empleados y facturas

---

## Notas Importantes

- Los modelos de Factura tienen relaciones con Empresa, Empleado y Servicio
- Los cálculos de subtotal y total se realizan automáticamente en el servicio
- Las validaciones se ejecutan en la capa de servicios (Tier 2)
- El frontend carga dinámicamente los datos de empresas, empleados y servicios para los dropdowns
- La base de datos se crea automáticamente al ejecutar la aplicación

---

## Próximos Pasos Sugeridos

1. Agregar más validaciones de negocio (ej: límite de facturas por empresa)
2. Implementar filtros y búsquedas avanzadas
3. Agregar reportes de facturas por empresa o empleado
4. Implementar autenticación y autorización
5. Agregar pruebas unitarias para los nuevos módulos
