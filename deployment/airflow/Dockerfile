FROM python:3.10-slim AS builder

WORKDIR /app

# Устанавливаем зависимости
COPY deployment/docker/requirements.txt .
RUN pip install --upgrade pip \
    && pip install --user --no-cache-dir -r requirements.txt \
    && pip install --user apache-airflow[celery]==2.7.2 pandas scikit-learn evidently mlflow

ENV PATH=/root/.local/bin:$PATH

COPY src/ src/
COPY scripts/ scripts/
COPY models/ models/

# Финальный образ
FROM python:3.10-slim

WORKDIR /app

RUN useradd -m appuser
USER appuser

COPY --from=builder /root/.local /home/appuser/.local
ENV PATH=/home/appuser/.local/bin:$PATH

COPY --from=builder /app/src ./src
COPY --from=builder /app/scripts ./scripts
COPY --from=builder /app/models ./models
COPY deployment/airflow/dags ./dags

CMD ["airflow", "standalone"]
