# Dockerfile para Backend - Tier 2: Lógica de Negocio
FROM python:3.11-slim

WORKDIR /app

# Instalar dependencias del sistema para PostgreSQL
RUN apt-get update && apt-get install -y \
    postgresql-client \
    libpq-dev \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copiar requirements
COPY requirements.txt .

# Instalar dependencias Python
RUN pip install --no-cache-dir -r requirements.txt && \
    pip install --no-cache-dir psycopg2-binary

# Copiar código de la aplicación
COPY . .

# Exponer puerto
EXPOSE 5001

# Comando por defecto
CMD ["python", "run.py"]



