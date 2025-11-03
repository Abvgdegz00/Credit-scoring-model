import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src")))
from features.build_features import build_features
import pandas as pd
import pytest


def make_valid_df():
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
            "default.payment.next.month": [0, 1],
        }
    )


def test_build_features_with_validation_data():
    df = make_valid_df()
    df_feat = build_features(df)

    # Проверяем что переименование работает
    assert "def_pay" in df_feat.columns
    assert "default.payment.next.month" not in df_feat.columns

    # Проверяем что ID удален если был
    if "ID" in df.columns:
        assert "ID" not in df_feat.columns


# Проверяем что данные содержат все необходимые колонки
def test_data_has_required_columns():
    df = make_valid_df()
    df_feat = build_features(df)

    required_columns = [
        "LIMIT_BAL",
        "AGE",
        "def_pay",
        "SEX",
        "EDUCATION",
        "MARRIAGE",
        "PAY_0",
        "PAY_2",
        "PAY_3",
        "PAY_4",
        "PAY_5",
        "PAY_6",
    ]

    for col in required_columns:
        assert col in df_feat.columns, f"Missing column: {col}"
