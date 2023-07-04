# Utiliza la imagen base de Python
FROM python:3.11.1

# Establece el directorio de trabajo en /app
WORKDIR /app

# Upgrade pip
RUN pip install --upgrade pip

#Install Git
RUN apt-get update && apt-get install -y git

# Copy the requirements file to the container
COPY requirements.txt .

# Install the project dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the project files to the container
COPY . .

# Expone el puerto 8080
EXPOSE 8080

# Ejecuta el comando para iniciar la aplicación
# uvicorn main:app --host 0.0.0.0 --port 8080
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]
