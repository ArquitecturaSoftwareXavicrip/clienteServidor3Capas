# Dockerfile para Frontend - Tier 1: Presentación
FROM node:18-alpine

WORKDIR /app

# Instalar dependencias del sistema
RUN apk add --no-cache bash

# Copiar package files
COPY package*.json ./

# Instalar dependencias
RUN npm install

# Copiar código de la aplicación
COPY . .

# Exponer puerto
EXPOSE 3001

# Variables de entorno
ENV CHOKIDAR_USEPOLLING=true
ENV WATCHPACK_POLLING=true
ENV PORT=3001
ENV HOST=0.0.0.0

# Comando por defecto
CMD ["npm", "start"]



