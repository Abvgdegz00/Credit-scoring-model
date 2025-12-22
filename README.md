# Credit Default Prediction

Полнофункциональный ML-пайплайн для предсказания дефолта клиентов кредитных карт.  

## 1. О проекте

**Задача:** бинарная классификация (дефолт / не дефолт) 
**Датасет:** [Default of Credit Card Clients Dataset](https://www.kaggle.com/datasets/uciml/default-of-credit-card-clients-dataset)
**Модели:** `GradientBoostingClassifier`, `RandomForestClassifier`, `XGBoostClassifier`


## 2. Архитектура проекта

```
credit-scoring-model/
├── .github/workflows/        # CI/CD пайплайны
├── data/
│   ├── raw/                  # Исходные данные
│   └── processed/            # Обработанные данные
├── deployment/
│   ├── airflow/              # DAGs и K8s конфиги для Airflow
│   ├── docker/               # Dockerfile и requirements для API, Drift, Trainer
│   └── kubernetes/           # K8s манифесты, AB-тестирование, monitoring, drift
├── docs/runbooks/            # Runbook документация
├── infrastructure/
│   ├── environments/         # Terraform конфигурации (staging, production)
│   ├── modules/              # Terraform модули (network, kubernetes, storage, monitoring)
│   └── scripts/              # Скрипты инициализации Terraform
├── models/                   # Обученные и конвертированные модели
├── notebooks/                # EDA
├── scripts/                  # Скрипты для обучения, конвертации, квантизации, бенчмарков
├── src/
│   ├── api/                  # FastAPI приложение
│   ├── create_models/        # Обучение, инференс, пайплайн, нейронная сеть
│   ├── data/                 # Подготовка и валидация данных
│   └── monitoring/           # Drift мониторинг
├── tests/                    # Unit-тесты
└── configuration files
```

## 3. Технологии

- **Версионирование данных:** DVC  
- **Трекинг экспериментов:** MLflow  
- **Валидация данных:** Great Expectations  
- **ML-пайплайн:** Scikit-learn / XGBoost  
- **Конвертация моделей:** ONNX + квантизация  
- **API:** FastAPI  
- **Контейнеризация:** Docker, multi-stage build  
- **Kubernetes:** Deployment, Service, liveness/readiness probes, NodeGroups  
- **CI/CD:** GitHub Actions (build, test, staging/production deploy, rollback)  
- **Тестирование:** pytest  
- **Мониторинг:** Prometheus, Grafana, Loki, Promtail  
- **Drift-мониторинг:** Evidently  
- **Автоматизация переобучения:** Airflow  

## 4. Руководство по установке и запуску

### 4.1. Клонирование и установка

```bash
git clone https://github.com/Abvgdegz00/Project-credit-scoring-model
cd credit-scoring-model
pip install -r requirements.txt
```

### 4.2. Запуск полного пайплайна

```bash
# Воспроизведение всего пайплайна
dvc repro

# Просмотр метрик
dvc metrics show

# Визуализация пайплайна
dvc dag
```

### 4.3. Запуск  

Проект содержит три Dockerfile для разных целей:

- **dockerfile.api:** приложение для предсказаний дефолта
- **dockerfile.drift:**	Контейнер для мониторинга drift модели с использованием Evidently
- **dockerfile.trainer:**	Контейнер для обучения моделей и конвертации/квантизации

#### 4.3.1. Сборка и запуск API
```bash
docker build -f deployment/docker/dockerfile.api -t credit-scoring-api .
docker run -p 8000:8000 credit-scoring-api
```

#### 4.3.2. Cборка и запуск Drift Monitoring
```bash
docker build -f deployment/docker/dockerfile.drift -t credit-drift-monitor .
docker run credit-drift-monitor
```

#### 4.3.3. Cборка и запуск Trainer
```bash
docker build -f deployment/docker/dockerfile.trainer -t credit-trainer .
docker run credit-trainer
```

### 4.4. Тестирование API

```bash
# Проверка
curl http://localhost:8000/health

# Пример предсказания
curl -X POST "http://localhost:8000/predict"   -H "Content-Type: application/json"   -d '{
    "LIMIT_BAL": 100000,
    "SEX": 1,
    "EDUCATION": 2,
    "MARRIAGE": 1,
    "AGE": 35,
    "PAY_0": 0,
    "PAY_2": 0,
    "PAY_3": 0,
    "PAY_4": 0,
    "PAY_5": 0,
    "PAY_6": 0,
    "BILL_AMT1": 1000,
    "BILL_AMT2": 1000,
    "BILL_AMT3": 1000,
    "BILL_AMT4": 1000,
    "BILL_AMT5": 1000,
    "BILL_AMT6": 1000,
    "PAY_AMT1": 1000,
    "PAY_AMT2": 1000,
    "PAY_AMT3": 1000,
    "PAY_AMT4": 1000,
    "PAY_AMT5": 1000,
    "PAY_AMT6": 1000
  }'
```

## 5. Структура кода

### 5.1. DVC-пайплайн
```yaml
stages:
  prepare:     # Подготовка данных
  train:       # Обучение модели
  convert:     # Конвертация и квантизация
  validate:    # Проверка совпадения результатов
```

## 6. Инфраструктура

- **Terraform модули:** network, kubernetes, storage, monitoring

- **Kubernetes:** Deployment, Service, liveness/readiness probes, NodeGroups

- **Мониторинг:** Prometheus + Grafana + Loki + алерты

- **Drift-мониторинг:** Evidently, деплоймент + ConfigMap

## 7. CI/CD

GitHub Actions автоматизирует:

- **Линтинг (black, flake8)**

- **Тестирование (pytest)**

- **Валидирует данные**

- **Build и push Docker образов**

- **Развертывание на staging / production**

- **Canary release и rollback**

## 8. Автоматическое переобучение

- **Airflow DAG для переобучения модели на новых данных**

- **Docker образ для Airflow**

- **Автоматическое масштабирование через K8s NodeGroups**

## 9. Мониторинг и алерты

- **CPU/Memory алерты через Terraform**

- **Centralized logging через Loki + Promtail**

- **Drift мониторинг с Evidently**