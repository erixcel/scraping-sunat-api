# Usamos una imagen base de Python
FROM python:3.9-slim-buster

# Para poder ver los print
ENV PYTHONUNBUFFERED 1

# Establecemos un directorio de trabajo
WORKDIR /app

# Copiamos el archivo requirements.txt al contenedor
COPY requirements.txt .

# Instalamos las dependencias
RUN pip install --no-cache-dir -r requirements.txt

# Instalamos las dependencias necesarias para Playwright
RUN apt-get update && apt-get install -y --fix-missing \
    libxcb-shm0 \
    libx11-xcb1 \
    libx11-6 \
    libxcb1 \
    libxext6 \
    libxrandr2 \
    libxcomposite1 \
    libxcursor1 \
    libxdamage1 \
    libxfixes3 \
    libxi6 \
    libgtk-3-0 \
    libpangocairo-1.0-0 \
    libpango-1.0-0 \
    libatk1.0-0 \
    libcairo-gobject2 \
    libcairo2 \
    libgdk-pixbuf2.0-0 \
    libglib2.0-0 \
    libasound2 \
    libxrender1 \
    libfreetype6 \
    libfontconfig1 \
    libdbus-1-3

# Instalamos los navegadores para Playwright
RUN python -m playwright install firefox

# Copiamos el resto del código de la aplicación al contenedor
COPY . .

# Exponemos el puerto en el que se ejecutará la aplicación
EXPOSE 5000

# Definimos el comando para ejecutar la aplicación
CMD ["python", "main.py"]
