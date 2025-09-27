# Imagen base oficial de Python
FROM python:3.10-slim

# Variables de entorno
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Crear directorio de la app
WORKDIR /app

# Copiar requirements y luego instalar (cache de Docker)
COPY requirements.txt /app/
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Copiar el resto del proyecto
COPY . /app/

# Exponer puerto de Django
EXPOSE 8000

# Migraciones automáticas y comando por defecto
CMD ["sh", "-c", "python manage.py makemigrations && python manage.py migrate && python manage.py runserver 0.0.0.0:8000"]
