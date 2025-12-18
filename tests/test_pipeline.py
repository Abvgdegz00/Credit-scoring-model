import pytest
import pandas as pd
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src")))
from create_models.pipeline import create_pipeline
from sklearn.ensemble import GradientBoostingClassifier, RandomForestClassifier
from xgboost import XGBClassifier


def make_sample_df():
    return pd.DataFrame(
        {
            "LIMIT_BAL": [100000, 200000],
            "AGE": [25, 35],
            "SEX": [1, 2],
            "EDUCATION": [1, 2],
            "MARRIAGE": [1, 1],
            "PAY_0": [0, 1],
            "PAY_2": [0, 1],
            "PAY_3": [0, 1],
            "PAY_4": [0, 1],
            "PAY_5": [0, 1],
            "PAY_6": [0, 1],
            "BILL_AMT1": [1000, 2000],
            "BILL_AMT2": [1000, 2000],
            "BILL_AMT3": [1000, 2000],
            "BILL_AMT4": [1000, 2000],
            "BILL_AMT5": [1000, 2000],
            "BILL_AMT6": [1000, 2000],
            "PAY_AMT1": [1000, 2000],
            "PAY_AMT2": [1000, 2000],
            "PAY_AMT3": [1000, 2000],
            "PAY_AMT4": [1000, 2000],
            "PAY_AMT5": [1000, 2000],
            "PAY_AMT6": [1000, 2000],
            "def_pay": [0, 1],
        }
    )


@pytest.mark.parametrize(
    "model_class", [GradientBoostingClassifier, RandomForestClassifier, XGBClassifier]
)
def test_pipeline_fit_predict(model_class):
    df = make_sample_df()
    X = df.drop("def_pay", axis=1)
    y = df["def_pay"]

    pipeline = create_pipeline(model_class(random_state=42))
    pipeline.fit(X, y)

    preds = pipeline.predict(X)
    proba = pipeline.predict_proba(X)[:, 1]

    # Проверяем размерность
    assert len(preds) == len(y)
    assert len(proba) == len(y)

    # Проверяем, что вероятности в диапазоне [0,1]
    assert all(0 <= p <= 1 for p in proba)


def test_pipeline_no_nan_in_output():
    df = make_sample_df()
    X = df.drop("def_pay", axis=1)
    y = df["def_pay"]

    pipeline = create_pipeline(GradientBoostingClassifier(random_state=42))
    pipeline.fit(X, y)
    proba = pipeline.predict_proba(X)[:, 1]

    # Проверяем, что нет NaN
    assert not pd.isna(proba).any()
