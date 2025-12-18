# Backend - Tier 2: Lógica de Negocio

Backend implementado con Flask siguiendo el patrón MVC y arquitectura de 3 capas.

## Estructura

```
backend/
├── app/
│   ├── __init__.py          # Factory de Flask app
│   ├── config/
│   │   └── database.py      # Configuración de BD
│   ├── controllers/         # Controladores MVC (Endpoints REST)
│   │   ├── empresa_controller.py
│   │   ├── servicio_controller.py
│   │   └── contrato_controller.py
│   ├── services/            # Lógica de negocio
│   │   ├── empresa_service.py
│   │   ├── servicio_service.py
│   │   └── contrato_service.py
│   ├── repositories/        # Tier 3: Acceso a datos
│   │   ├── empresa_repository.py
│   │   ├── servicio_repository.py
│   │   └── contrato_repository.py
│   └── models/              # Modelos de dominio
│       ├── empresa.py
│       ├── servicio.py
│       └── contrato.py
├── requirements.txt
├── run.py
└── README.md
```

## Instalación

```bash
python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate
pip install -r requirements.txt
```

## Ejecución

```bash
python run.py
```

La API estará disponible en `http://localhost:5000`

## Endpoints

Ver README.md principal para la documentación completa de endpoints.



