import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src")))
from features.build_features import build_features
import pandas as pd
import pytest


def test_build_features_removes_id():
    df = pd.DataFrame(
        {
            "ID": [1, 2],
            "SEX": [1, 2],
            "default.payment.next.month": [0, 1],
        }
    )
    df_feat = build_features(df)
    assert "ID" not in df_feat.columns


def test_build_features_preserves_other_columns():
    df = pd.DataFrame(
        {
            "ID": [1, 2],
            "SEX": [1, 2],
            "AGE": [25, 30],
            "default.payment.next.month": [0, 1],
        }
    )
    df_feat = build_features(df)
    assert "SEX" in df_feat.columns
    assert "AGE" in df_feat.columns
    assert "def_pay" in df_feat.columns


def test_build_features_renames_target():
    df = pd.DataFrame(
        {
            "ID": [1, 2],
            "default.payment.next.month": [0, 1],
        }
    )
    df_feat = build_features(df)
    assert "def_pay" in df_feat.columns
    assert "default.payment.next.month" not in df_feat.columns
