import pandas as pd


def build_features(df: pd.DataFrame) -> pd.DataFrame:

    df = df.copy()

    # Удалим ненужную колонку ID, если она есть
    if "ID" in df.columns:
        df.drop(columns=["ID"], inplace=True)

    # Переименование целевой переменной
    if "default.payment.next.month" in df.columns:
        df.rename(columns={"default.payment.next.month": "def_pay"}, inplace=True)

    return df
