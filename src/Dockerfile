FROM python:3.11-slim

WORKDIR /app

# Evita prompts interativos e reduz layers
ENV DEBIAN_FRONTEND=noninteractive

# Instala apenas o necessário pro sentence-transformers
RUN apt-get update && apt-get install -y \
    build-essential \
    git \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# Copia só o requirements antes pro cache funcionar
COPY ../requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

# Copia o código por último (evita rebuild de dependências quando só o código muda)
COPY src /app/src

ENV PYTHONPATH=/app/src

CMD ["uvicorn", "src.app:app", "--host", "0.0.0.0", "--port", "8000"]