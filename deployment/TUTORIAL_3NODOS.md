# Tutorial Completo - Despliegue en 3 Nodos

## 📋 Información de los 3 Nodos

| Node | IP Real | SO | Servicio | Puerto |
|------|---------|----|----|--------|
| **Node 1** | 172.17.162.45 | Windows | PostgreSQL Database | 5433 |
| **Node 2** | 172.17.188.98 | Windows | Flask Backend API | 5001 |
| **Node 3** | 172.17.187.8 | Mac | React Frontend | 3001 |

---

## 🚀 Paso 1: Clonar el Repositorio en las 3 Máquinas

**En TODAS las máquinas (Node 1, Node 2, Node 3):**

```bash
git clone https://github.com/tu-usuario/clienteServidor3Capas.git
cd clienteServidor3Capas
```

---

## 🔧 Paso 2: Configuración de Node 1 (Database - 172.17.162.45)

### En la máquina Windows con IP 172.17.162.45:

**No hay archivos que editar en Node 1.** Solo necesita que Docker esté corriendo.

Ejecuta:

```bash
docker-compose up --build
```

**Verificar que está corriendo:**

```bash
docker ps | findstr "limpieza_db"
```

Deberías ver:
```
limpieza_db    postgres:15-alpine    Up    0.0.0.0:5433->5432/tcp
```

---

## 🔧 Paso 3: Configuración de Node 2 (Backend - 172.17.188.98)

### En la máquina Windows con IP 172.17.188.98:

**Editar archivo: `backend/.env`**

Abre el archivo `backend/.env` y reemplaza el contenido con:

```env
FLASK_ENV=production
SQLALCHEMY_DATABASE_URI=postgresql://limpieza_user:contraseña_segura_123@172.17.162.45:5433/limpieza_empresas
PORT=5001
SECRET_KEY=tu-clave-secreta-super-segura-aqui-cambiar-en-produccion
CORS_ORIGINS=http://172.17.187.8:3001,http://localhost:3001
```

**Importante:** Cambiar `172.17.162.45` por la IP real de Node 1 si es diferente.

Luego ejecuta:

```bash
docker-compose up --build
```

**Verificar que está corriendo:**

```bash
docker ps | findstr "limpieza_backend"
```

Deberías ver:
```
limpieza_backend    Flask API    Up    0.0.0.0:5001->5001/tcp
```

---

## 🔧 Paso 4: Configuración de Node 3 (Frontend - 172.17.187.8 - Mac)

### En tu Mac con IP 172.17.187.8:

**Editar archivo 1: `frontend/.env`**

Abre el archivo `frontend/.env` y reemplaza el contenido con:

```env
PORT=3001
HOST=0.0.0.0
DANGEROUSLY_DISABLE_HOST_CHECK=true
REACT_APP_API_URL=http://172.17.188.98:5001/api
```

**Importante:** Cambiar `172.17.188.98` por la IP real de Node 2 si es diferente.

---

**Editar archivo 2: `frontend/src/config.js`**

Crea un nuevo archivo `frontend/src/config.js` con este contenido:

```javascript
/**
 * Configuración de la aplicación
 * Lee la URL de la API del Backend
 */

const API_URL = 
  process.env.REACT_APP_API_URL || 
  (typeof window !== 'undefined' && window.API_URL) || 
  'http://localhost:5001/api';

console.log('API URL configurada:', API_URL);

export const config = {
  API_URL: API_URL,
};

export default config;
```

---

**Editar archivo 3: `frontend/src/services/api.js`**

Abre el archivo `frontend/src/services/api.js` y reemplaza las primeras líneas:

**Busca esto:**
```javascript
import axios from 'axios';

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:5001/api';
```

**Reemplaza con esto:**
```javascript
import axios from 'axios';
import { config } from '../config';

const API_BASE_URL = config.API_URL;
```

---

**Editar archivo 4: `frontend/package.json`**

Abre el archivo `frontend/package.json` y busca la línea:

```json
"proxy": "http://localhost:5001"
```

**Elimina esa línea completamente.** El archivo debe terminar así:

```json
  "browserslist": {
    "production": [
      ">0.2%",
      "not dead",
      "not op_mini all"
    ],
    "development": [
      "last 1 chrome version",
      "last 1 firefox version",
      "last 1 safari version"
    ]
  }
}
```

---

Luego ejecuta:

```bash
docker-compose up --build
```

**Verificar que está corriendo:**

```bash
docker ps | grep limpieza_frontend
```

Deberías ver:
```
limpieza_frontend    React App    Up    0.0.0.0:3001->3001/tcp
```

---

## ✅ Paso 5: Verificar que Todo Funciona

### Desde Node 3 (Tu Mac):

**Opción 1: Acceso Local**
```
http://localhost:3001
```

**Opción 2: Acceso desde la Red**
```
http://172.17.187.8:3001
```

---

### Desde Node 1 o Node 2 (Windows):

**Acceso al Frontend:**
```
http://172.17.187.8:3001
```

**Acceso al Backend API:**
```
http://172.17.188.98:5001/api/empresas
```

---

## 🧪 Pruebas Finales

### 1. Crear una Empresa desde el Frontend

1. Abre http://localhost:3001 (o http://172.17.187.8:3001)
2. Completa el formulario:
   - Nombre: Test Company
   - Dirección: Calle Principal 123
   - Teléfono: 0912345678
   - Email: test@company.com
3. Haz clic en "Crear"

### 2. Verificar que se guardó en la Database (Node 1)

Desde Node 1 (Windows), ejecuta:

```bash
docker exec -it limpieza_db psql -U limpieza_user -d limpieza_empresas -c "SELECT * FROM empresas;"
```

Deberías ver la empresa que creaste.

### 3. Verificar Logs del Backend (Node 2)

Desde Node 2 (Windows), ejecuta:

```bash
docker logs limpieza_backend --tail 20
```

Deberías ver:
```
POST /api/empresas HTTP/1.1 201
```

---

## 📊 Resumen de Cambios por Máquina

### Node 1 (172.17.162.45 - Windows)
- ✅ Sin cambios necesarios
- ✅ Solo ejecutar: `docker-compose up --build`

### Node 2 (172.17.188.98 - Windows)
- ✅ Editar: `backend/.env`
  - Cambiar `SQLALCHEMY_DATABASE_URI` con IP de Node 1
  - Cambiar `CORS_ORIGINS` con IP de Node 3
- ✅ Ejecutar: `docker-compose up --build`

### Node 3 (172.17.187.8 - Mac)
- ✅ Editar: `frontend/.env`
  - Cambiar `REACT_APP_API_URL` con IP de Node 2
- ✅ Crear: `frontend/src/config.js` (nuevo archivo)
- ✅ Editar: `frontend/src/services/api.js`
  - Cambiar importación para usar config.js
- ✅ Editar: `frontend/package.json`
  - Eliminar línea `"proxy": "http://localhost:5001"`
- ✅ Ejecutar: `docker-compose up --build`

---

## 🔗 URLs de Acceso Final

| Servicio | URL |
|----------|-----|
| Frontend (desde tu Mac) | http://localhost:3001 |
| Frontend (desde la red) | http://172.17.187.8:3001 |
| Backend API | http://172.17.188.98:5001/api/empresas |
| Database | 172.17.162.45:5433 |

---

## 🆘 Troubleshooting

### Error: "Cannot connect to database"
- Verificar que Node 1 está corriendo: `docker ps | findstr "limpieza_db"`
- Verificar que la IP en `backend/.env` es correcta

### Error: "Cannot connect to backend"
- Verificar que Node 2 está corriendo: `docker ps | findstr "limpieza_backend"`
- Verificar que la IP en `frontend/.env` es correcta

### Error: "CORS policy blocked"
- Verificar que `CORS_ORIGINS` en `backend/.env` incluye la IP de Node 3
- Reconstruir el Frontend: `docker-compose down && docker-compose up --build`

### Error: "Frontend shows 'Not Found'"
- Acceder a `http://localhost:3001` en lugar de la IP
- O reconstruir: `docker-compose down && docker-compose up --build`

---

## 📝 Checklist Final

**Node 1 (172.17.162.45):**
- [ ] Cloné el repositorio
- [ ] Ejecuté `docker-compose up --build`
- [ ] Verifiqué que `limpieza_db` está corriendo

**Node 2 (172.17.188.98):**
- [ ] Cloné el repositorio
- [ ] Edité `backend/.env` con IP de Node 1
- [ ] Ejecuté `docker-compose up --build`
- [ ] Verifiqué que `limpieza_backend` está corriendo

**Node 3 (172.17.187.8 - Mac):**
- [ ] Cloné el repositorio
- [ ] Edité `frontend/.env` con IP de Node 2
- [ ] Creé `frontend/src/config.js`
- [ ] Edité `frontend/src/services/api.js`
- [ ] Edité `frontend/package.json` (eliminé proxy)
- [ ] Ejecuté `docker-compose up --build`
- [ ] Verifiqué que `limpieza_frontend` está corriendo
- [ ] Accedí a http://localhost:3001 y verifiqué que funciona

---

**¡Listo! El despliegue en 3 nodos está completamente configurado.**
