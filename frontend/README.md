# Frontend - Tier 1: Presentación

Frontend implementado con React siguiendo el patrón MVC y arquitectura de 3 capas.

## Estructura

```
frontend/
├── public/
│   └── index.html
├── src/
│   ├── views/              # Vistas MVC (Componentes React)
│   │   ├── EmpresaView.js
│   │   ├── ServicioView.js
│   │   └── ContratoView.js
│   ├── services/           # Cliente API (comunicación con backend)
│   │   └── api.js
│   ├── App.js              # Componente principal
│   ├── index.js            # Punto de entrada
│   └── index.css           # Estilos globales
├── package.json
└── README.md
```

## Instalación

```bash
npm install
```

## Ejecución

```bash
npm start
```

La aplicación estará disponible en `http://localhost:3000`

## Características

- Interfaz de usuario moderna y responsive
- Gestión completa de CRUD para Empresas, Servicios y Contratos
- Comunicación con backend mediante API REST
- Validación de formularios
- Manejo de errores y mensajes de éxito


