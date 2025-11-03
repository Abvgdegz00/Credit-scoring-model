from fastapi import FastAPI
from pydantic import BaseModel
import pandas as pd
import joblib
from src.features.build_features import build_features
from pathlib import Path

MODEL_PATH = Path("/app/models/credit_default_model.pkl")

# Создание приложения
app = FastAPI(title="Credit Default Prediction API")

# Загрузка модели
try:
    model = joblib.load(MODEL_PATH)
    print(f"Модель загружена из: {MODEL_PATH}")
except FileNotFoundError:
    print(f"Модель не найдена по пути: {MODEL_PATH}")
    model = None


# Описание входных данных
class ClientData(BaseModel):
    LIMIT_BAL: float
    SEX: int
    EDUCATION: int
    MARRIAGE: int
    AGE: int
    PAY_0: int
    PAY_2: int
    PAY_3: int
    PAY_4: int
    PAY_5: int
    PAY_6: int
    BILL_AMT1: float
    BILL_AMT2: float
    BILL_AMT3: float
    BILL_AMT4: float
    BILL_AMT5: float
    BILL_AMT6: float
    PAY_AMT1: float
    PAY_AMT2: float
    PAY_AMT3: float
    PAY_AMT4: float
    PAY_AMT5: float
    PAY_AMT6: float


# Endpoint для предсказаний
@app.post("/predict")
def predict_endpoint(data: ClientData):
    if model is None:
        return {"error": "Модель не загружена"}

    input_df = pd.DataFrame([data.dict()])
    df_feat = build_features(input_df)
    pred = model.predict(df_feat)[0]
    proba = model.predict_proba(df_feat)[0][1]
    return {"default_prediction": int(pred), "default_probability": float(proba)}


# Проверочный endpoint
@app.get("/")
def read_root():
    return {"message": "Credit Default Prediction API is alive!"}


# Health check endpoint для мониторинга
@app.get("/health")
def health_check():
    return {"status": "healthy", "model_loaded": model is not None}
