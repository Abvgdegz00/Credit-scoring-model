FROM python:3.9-slim

# Зависимости
RUN apt-get update && \
    apt-get install -y --no-install-recommends build-essential && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Копируем requirements
COPY requirements.txt ./

# Зависимости Python
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN mkdir -p /app/models
COPY models/credit_default_model.pkl /app/models/credit_default_model.pkl

RUN ls -la /app/models/ && \
    find /app -name "credit_default_model.pkl" -type f

# Порт для FastAPI
EXPOSE 8000

# FastAPI
CMD ["uvicorn", "src.api.app:app", "--host", "0.0.0.0", "--port", "8000"]