# Dockerfile
FROM python:3.12-slim

#Instalar dependencias del sistema mínimas.
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    && rm -rf /var/lib/apt/lists/*

#Instalación de uv
RUN curl -LsSf https://astral.sh/uv/install.sh | sh

# Añadir uv al PATH (la instalación lo mete en /root/.local/bin, y así esta en el sitio correcto).
ENV PATH="/root/.local/bin:${PATH}"

#Crear sitio de trabajo.
WORKDIR /app

COPY pyproject.toml uv.lock* ./

RUN uv sync --frozen || uv sync

# Copiar el resto del código.
COPY . .

# Exponer el puerto que usa Gradio (por defecto 7860)
EXPOSE 7860

# Comando usado por mi para ejecutar la aplicación.
CMD ["uv", "run", "python", "app.py"]
