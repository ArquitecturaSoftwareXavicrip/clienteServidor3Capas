  # Documentación de Arquitectura

## Arquitectura Cliente-Servidor y 3 Capas

Esta aplicación implementa dos estilos arquitectónicos principales:

### 1. Arquitectura Cliente-Servidor

- **Cliente (Frontend)**: Aplicación React que se ejecuta en el navegador del usuario
- **Servidor (Backend)**: API REST implementada con Flask que procesa las peticiones

**Comunicación**: HTTP/REST mediante JSON

### 2. Arquitectura de 3 Capas (3-Tier)

La aplicación está dividida en tres capas lógicas que pueden desplegarse en tiers físicos separados:

#### Tier 1: Capa de Presentación (Frontend)
- **Ubicación**: `frontend/`
- **Tecnología**: React + JavaScript
- **Responsabilidades**:
  - Interfaz de usuario (Views)
  - Captura de eventos del usuario
  - Comunicación con el backend vía HTTP
  - Renderizado de datos
- **Componentes principales**:
  - `views/EmpresaView.js` - Vista de empresas
  - `views/ServicioView.js` - Vista de servicios
  - `views/ContratoView.js` - Vista de contratos
  - `services/api.js` - Cliente HTTP para comunicación con backend

#### Tier 2: Capa de Lógica de Negocio (Backend)
- **Ubicación**: `backend/app/`
- **Tecnología**: Flask (Python)
- **Responsabilidades**:
  - Controladores MVC que manejan requests HTTP
  - Servicios de negocio (validaciones, reglas de negocio)
  - Coordinación entre capas
- **Estructura**:
  - `controllers/` - Controladores MVC (Endpoints REST)
  - `services/` - Lógica de negocio (validaciones, cálculos)
  - `repositories/` - Acceso a datos (llamadas a Tier 3)

#### Tier 3: Capa de Acceso a Datos (Database)
- **Ubicación**: `backend/app/repositories/` y `backend/app/models/`
- **Tecnología**: SQLite + SQLAlchemy ORM
- **Responsabilidades**:
  - Repositorios que encapsulan acceso a BD
  - Modelos de datos
  - Operaciones CRUD
- **Componentes principales**:
  - `models/` - Modelos de dominio (Empresa, Servicio, Contrato)
  - `repositories/` - Repositorios con operaciones CRUD
  - `config/database.py` - Configuración de conexión

## Patrón MVC

El patrón Modelo-Vista-Controlador está implementado en cada capa:

### En el Frontend (Tier 1):
- **Model**: Estructuras de datos en los componentes React
- **View**: Componentes React (`EmpresaView`, `ServicioView`, `ContratoView`)
- **Controller**: Lógica de manejo de eventos y comunicación con API

### En el Backend (Tier 2):
- **Model**: Modelos de dominio en `models/`
- **View**: Respuestas JSON de la API
- **Controller**: Controladores en `controllers/` que manejan endpoints REST

## Flujo de Datos

```
Usuario (Browser)
    ↓
Frontend - View (React Component)
    ↓ [HTTP Request]
Frontend - API Service (api.js)
    ↓ [HTTP/REST]
Backend - Controller (empresa_controller.py)
    ↓
Backend - Service (empresa_service.py) [Validaciones, Lógica de Negocio]
    ↓
Backend - Repository (empresa_repository.py)
    ↓ [SQL]
Database (SQLite)
    ↓ [Datos]
Repository (retorna objetos Model)
    ↓
Service (procesa y valida)
    ↓
Controller (formatea respuesta JSON)
    ↓ [HTTP Response]
Frontend - API Service (recibe respuesta)
    ↓
Frontend - View (actualiza UI)
    ↓
Usuario (ve resultado)
```

## Separación de Responsabilidades

### Frontend (Tier 1)
- NO contiene lógica de negocio
- NO accede directamente a la base de datos
- Solo se comunica con el backend mediante API REST

### Backend - Controllers (Tier 2)
- Manejan peticiones HTTP
- Validan formato de datos
- Delegan lógica de negocio a Services
- Formatean respuestas

### Backend - Services (Tier 2)
- Contienen toda la lógica de negocio
- Validaciones de reglas de negocio
- Cálculos y transformaciones
- NO acceden directamente a la BD (usan Repositories)

### Backend - Repositories (Tier 3)
- Encapsulan acceso a datos
- Operaciones CRUD
- NO contienen lógica de negocio
- Retornan objetos Model

## Despliegue Multi-Tier

Cada tier puede desplegarse en servidores físicos diferentes:

1. **Tier 1 (Frontend)**: Servidor web estático o CDN
2. **Tier 2 (Backend)**: Servidor de aplicaciones (puede escalar horizontalmente)
3. **Tier 3 (Database)**: Servidor de base de datos dedicado

Con Docker Compose, cada tier corre en un contenedor separado, demostrando la separación física.

## Ventajas de esta Arquitectura

1. **Separación de responsabilidades**: Cada capa tiene un propósito claro
2. **Escalabilidad**: Cada tier puede escalarse independientemente
3. **Mantenibilidad**: Cambios en una capa no afectan directamente a otras
4. **Testabilidad**: Cada capa puede probarse de forma independiente
5. **Reutilización**: La API puede ser consumida por diferentes clientes (web, móvil, etc.)


