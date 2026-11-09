# Imagen base oficial de Python ligera
FROM python:3.12-slim

# Evitar escritura de archivos .pyc y habilitar salida en tiempo real
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONPATH=/app

# Establecer directorio de trabajo
WORKDIR /app

# Instalar dependencias del sistema necesarias
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copiar archivo de requerimientos e instalar dependencias de Python
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copiar el código fuente del proyecto
COPY . .

# Crear y usar un usuario sin privilegios por seguridad
RUN useradd -m appuser && chown -R appuser:appuser /app
USER appuser

# Comando por defecto: ejecutar la aplicación principal
CMD ["python", "main.py"]
