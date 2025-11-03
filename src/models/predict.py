import pandas as pd
import joblib
from src.features.build_features import build_features


# Загружаем модель
model = joblib.load('models/credit_default_model.pkl')


def predict(input_df: pd.DataFrame):
    df_processed = build_features(input_df)
    pred = model.predict(df_processed)
    proba = model.predict_proba(df_processed)[:, 1]
    return pred, proba
