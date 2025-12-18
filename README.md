# Credit Default Prediction

Полнофункциональный ML-пайплайн для предсказания дефолта клиентов кредитных карт.  

## 1. О проекте

**Задача:** бинарная классификация (дефолт / не дефолт) 
**Датасет:** [Default of Credit Card Clients Dataset](https://www.kaggle.com/datasets/uciml/default-of-credit-card-clients-dataset)
**Модели:** `GradientBoostingClassifier`, `RandomForestClassifier`, `XGBoostClassifier`


## 2. Архитектура проекта

```
credit-scoring-model/
├── data/
│   ├── raw/                    # Исходные данные (DVC)
│   └── processed/              # Обработанные данные (DVC)
├── models/                     # Обученные модели (DVC)
├── src/
│   ├── data/                   # Подготовка и валидация данных
│   ├── create_models/          # Обучение и предсказание
│   └── api/                    # FastAPI приложение
├── tests/                      # Unit-тесты
├── notebooks/                  # EDA
├── .github/workflows/          # CI/CD пайплайны
└── configuration files
```

## 3. Технологии

- **Версионирование данных:** DVC  
- **Трекинг экспериментов:** MLflow  
- **Валидация данных:** Great Expectations  
- **ML-пайплайн:** Scikit-learn / XGBoost
- **API:** FastAPI  
- **Контейнеризация:** Docker  
- **CI/CD:** GitHub Actions  
- **Тестирование:** pytest  

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

### 4.3. Запуск API

```bash
# Сборка Docker образа
docker build -t credit-scoring-api .

# Запуск контейнера
docker run -p 8000:8000 credit-scoring-api
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

### 5.1. Основные модули

| Модуль | Назначение |
|--------|-------------|
| `src/data/make_dataset.py` | Подготовка и разделение данных |
| `src/data/validation.py` | Валидация данных |
| `src/create_models/pipeline.py` | Создание ML пайплайна |
| `src/create_models/train.py` | Обучение модели и логирование в MLflow |
| `src/create_models/predict.py` | Инференс |
| `src/api/app.py` | FastAPI приложение |

### 5.2. DVC-пайплайн
```yaml
stages:
  prepare:     # Подготовка данных
  train:       # Обучение модели
```

## 6. Разработка

### 6.1. Запуск тестов
```bash
pytest tests/ -v
```

### 6.2. Линтинг кода
```bash
black src tests
flake8 src tests
```

### 6.3. Переобучение модели
```bash
dvc repro train
```

### 6.4. Мониторинг экспериментов
```bash
mlflow ui
# Открыть http://localhost:5000
```

## 7. API Документация

После запуска API доступно:

- **Swagger UI:** [http://localhost:8000/docs](http://localhost:8000/docs)  
- **ReDoc:** [http://localhost:8000/redoc](http://localhost:8000/redoc)

### Эндпоинты
| Метод | Путь | Назначение |
|--------|------|-------------|
| `GET` | `/` | Статус API |
| `GET` | `/health` | Проверка здоровья |
| `POST` | `/predict` | Предсказание дефолта |

## 8. Воспроизведение пайплайна
```bash
dvc repro
```

## 9. CI/CD

GitHub Actions автоматически:

- Запускает тесты  
- Проверяет качество кода (`black`, `flake8`)  
- Валидирует данные

## 10. Docker

Проект поставляется с Dockerfile для локального запуска FastAPI приложения

### Сборка Docker образа
```bash
docker build -t credit-scoring-api .
```

### Запуск контейнера
```bash
docker run -p 8000:8000 credit-scoring-api
```

### Описание образа:

- **Базовый образ:** python:3.9-slim

- Устанавливаются зависимости из requirements.txt

- Копируются исходный код и обученная модель credit_default_model.pkl

- Порт FastAPI: 8000

**Команда запуска:**
```bash
uvicorn src.api.app:app --host 0.0.0.0 --port 8000
```

### Проверка доступности API
```bash
curl http://localhost:8000/health
```