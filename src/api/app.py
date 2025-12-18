from fastapi import FastAPI
from pydantic import BaseModel
import pandas as pd
import joblib
from pathlib import Path

MODEL_PATH = Path("/app/models/credit_default_model.pkl")

app = FastAPI(title="Credit Default Prediction API")

try:
    model = joblib.load(MODEL_PATH)
except FileNotFoundError:
    model = None


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


@app.post("/predict")
def predict_endpoint(data: ClientData):
    if model is None:
        return {"error": "Model not loaded"}

    input_df = pd.DataFrame([data.dict()])
    pred = model.predict(input_df)[0]
    proba = model.predict_proba(input_df)[0][1]

    return {
        "default_prediction": int(pred),
        "default_probability": float(proba),
    }


@app.get("/")
def read_root():
    return {"message": "Credit Default Prediction API is alive!"}


@app.get("/health")
def health_check():
    return {"status": "healthy", "model_loaded": model is not None}
