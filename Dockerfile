# Usa una imagen base de Python 3.11
FROM python:3.11-slim

RUN apt-get update && apt-get install -y pkg-config

# Establece el directorio de trabajo en /app
WORKDIR /app

# Copia el archivo de requerimientos (requirements.txt) a la imagen
COPY requirements.txt requirements.txt

# Instala las dependencias del proyecto
RUN pip install --no-cache-dir -r requirements.txt

# Copia todo el contenido del directorio actual al directorio /app en la imagen
COPY . .

# Expone el puerto en el que tu aplicación se ejecutará
EXPOSE 80

# Ejecuta la aplicación
CMD ["uvicorn", "main:app", "--reload", "--host", "0.0.0.0", "--port", "80"]

