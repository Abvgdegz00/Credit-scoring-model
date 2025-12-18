import pandas as pd
import joblib

# Загружаем модель
model = joblib.load("models/credit_default_model.pkl")


def predict(input_df: pd.DataFrame):
    pred = model.predict(input_df)
    proba = model.predict_proba(input_df)[:, 1]
    return pred, proba
