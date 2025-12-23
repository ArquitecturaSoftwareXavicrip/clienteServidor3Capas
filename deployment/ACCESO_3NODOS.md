# Acceso a los 3 Nodos - Guía de Conexión

## 📍 IPs Reales de los 3 Nodos

```
Node 1 (Database)  : 172.17.162.45:5433
Node 2 (Backend)   : 172.17.188.98:5001
Node 3 (Frontend)  : 172.17.187.8:3001
```

---

## 🌐 Links de Acceso

### Desde cualquier máquina en la red local

**Frontend (Interfaz de Usuario)**
```
http://172.17.187.8:3001
```

**Backend API (Para verificar)**
```
http://172.17.188.98:5001/api/empresas
```

**Database (PostgreSQL)**
```
Host: 172.17.162.45
Puerto: 5433
Usuario: limpieza_user
Contraseña: contraseña_segura_123
Base de datos: limpieza_empresas
```

---

## 📋 Flujo de Comunicación

```
Tu Navegador (cualquier máquina)
    ↓
http://172.17.187.8:3001 (Node 3 - Frontend)
    ↓
http://172.17.188.98:5001/api (Node 2 - Backend)
    ↓
postgresql://172.17.162.45:5433 (Node 1 - Database)
    ↓
Datos persistidos ✅
```

---

## ✅ Verificación de Conectividad

### Desde Node 1 (Database)
```bash
# Verificar que PostgreSQL está corriendo
docker ps | findstr "limpieza_db"

# Acceder a la BD
docker exec -it limpieza_db psql -U limpieza_user -d limpieza_empresas -c "SELECT * FROM empresas;"
```

### Desde Node 2 (Backend)
```bash
# Verificar que Backend está corriendo
docker ps | findstr "limpieza_backend"

# Probar API
curl http://172.17.188.98:5001/api/empresas

# Ver logs
docker logs limpieza_backend -f
```

### Desde Node 3 (Frontend - Tu Mac)
```bash
# Verificar que Frontend está corriendo
docker ps | grep limpieza_frontend

# Abrir en navegador
http://172.17.187.8:3001
```

---

## 🧪 Prueba Completa del Flujo

### Paso 1: Abrir Frontend
Abre en tu navegador: **http://172.17.187.8:3001**

### Paso 2: Crear una Empresa
Completa el formulario:
- Nombre: Test Company
- Dirección: Calle Principal 456
- Teléfono: 0987654321
- Email: test@company.com

Haz clic en "Crear"

### Paso 3: Verificar en Database (Node 1)
```bash
docker exec -it limpieza_db psql -U limpieza_user -d limpieza_empresas -c "SELECT * FROM empresas;"
```

Deberías ver la empresa que creaste.

### Paso 4: Verificar Logs (Node 2)
```bash
docker logs limpieza_backend --tail 20
```

Deberías ver:
```
POST /api/empresas HTTP/1.1 201
```

---

## 🔧 Configuración de Archivos .env

### backend/.env (ubicado en Node 3)
```env
FLASK_ENV=production
SQLALCHEMY_DATABASE_URI=postgresql://limpieza_user:contraseña_segura_123@172.17.162.45:5433/limpieza_empresas
PORT=5001
SECRET_KEY=tu-clave-secreta-super-segura-aqui-cambiar-en-produccion
CORS_ORIGINS=http://172.17.187.8:3001,http://localhost:3001
```

### frontend/.env (ubicado en Node 3)
```env
PORT=3001
HOST=0.0.0.0
DANGEROUSLY_DISABLE_HOST_CHECK=true
REACT_APP_API_URL=http://172.17.188.98:5001/api
```

---

## 📊 Estado de Contenedores

### Node 1 (172.17.162.45)
```bash
docker ps | findstr "limpieza_db"
# Debe mostrar: limpieza_db Up (healthy)
```

### Node 2 (172.17.188.98)
```bash
docker ps | findstr "limpieza_backend"
# Debe mostrar: limpieza_backend Up
```

### Node 3 (172.17.187.8)
```bash
docker ps | grep limpieza_frontend
# Debe mostrar: limpieza_frontend Up
```

---

## 🚀 Reiniciar Contenedores

Si necesitas reiniciar los contenedores en cualquier nodo:

```bash
# Detener
docker-compose down

# Reiniciar
docker-compose up --build
```

---

## 🐛 Troubleshooting

### Error: "Cannot connect to database"
- Verificar que Node 1 está corriendo: `docker ps | findstr "limpieza_db"`
- Verificar que la IP en backend/.env es correcta: `172.17.162.45:5433`
- Verificar que el puerto 5433 está abierto en Node 1

### Error: "Cannot connect to backend"
- Verificar que Node 2 está corriendo: `docker ps | findstr "limpieza_backend"`
- Verificar que la IP en frontend/.env es correcta: `172.17.188.98:5001`
- Verificar que el puerto 5001 está abierto en Node 2

### Error: "CORS error"
- Verificar que CORS_ORIGINS en backend/.env incluye la IP de Node 3: `http://172.17.187.8:3001`

### Error: "Frontend no carga"
- Verificar que Node 3 está corriendo: `docker ps | grep limpieza_frontend`
- Verificar que el puerto 3001 está abierto en Node 3
- Limpiar caché del navegador (Ctrl+Shift+Delete)

---

## 📞 Contacto y Soporte

Si tienes problemas:

1. Verifica que todos los contenedores están corriendo: `docker ps`
2. Revisa los logs: `docker logs [nombre_contenedor]`
3. Verifica la conectividad: `curl http://[IP]:[PUERTO]`
4. Reinicia los contenedores: `docker-compose down && docker-compose up --build`

---

## ✨ Resumen Rápido

| Acción | Comando/Link |
|--------|-------------|
| Abrir Frontend | http://172.17.187.8:3001 |
| Probar API | curl http://172.17.188.98:5001/api/empresas |
| Ver BD | docker exec -it limpieza_db psql -U limpieza_user -d limpieza_empresas |
| Ver logs Backend | docker logs limpieza_backend -f |
| Ver logs Frontend | docker logs limpieza_frontend -f |
| Reiniciar todo | docker-compose down && docker-compose up --build |
