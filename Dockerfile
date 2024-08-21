# Etapa 1: Construcción de las dependencias de Python y las bibliotecas necesarias
FROM python:3.9-slim AS builder

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set the working directory in the container
WORKDIR /app

# Install system dependencies for building Python packages
RUN apt-get update && apt-get install -y \
    build-essential \
    libssl-dev \
    libffi-dev \
    libxml2-dev \
    libxslt1-dev \
    libjpeg-dev \
    zlib1g-dev \
    libpango1.0-dev \
    libcairo2 \
    libgdk-pixbuf2.0-0 \
    libgirepository1.0-dev \
    gir1.2-pango-1.0 \
    shared-mime-info \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copia todos los archivos de la aplicación
COPY . .

# Collect static files (assuming you need this for your Django app)
RUN python manage.py collectstatic --noinput

# Etapa 2: Imagen final más pequeña sin herramientas de construcción
FROM python:3.9-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set the working directory in the container
WORKDIR /app

# Copy the dependencies from the builder stage
COPY --from=builder /usr/local/lib/python3.9/site-packages /usr/local/lib/python3.9/site-packages
COPY --from=builder /app /app

# Copy the static files from the builder stage
COPY --from=builder /app/static /app/static

# Install runtime dependencies
RUN apt-get update && apt-get install -y \
    libcairo2 \
    libgdk-pixbuf2.0-0 \
    libpango1.0-0 \
    && rm -rf /var/lib/apt/lists/*

# Expose the port Django runs on
EXPOSE 8000

# Run the application
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
