# Imagen oficial de Python ligera
FROM python:3.12-slim

# Evita que Python escriba archivos .pyc y forza la salida estándar en consola
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Establece el directorio de trabajo
WORKDIR /app

# Instala dependencias
COPY requirements.txt /app/
RUN pip install --upgrade pip && pip install -r requirements.txt

# El código se montará como volumen, pero copiamos lo actual por si acaso
COPY . /app/