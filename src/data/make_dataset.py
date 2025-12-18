import pandas as pd
import sys
from sklearn.model_selection import train_test_split
from pathlib import Path


def prepare_dataset(input_path: str, output_dir: str, test_size: float = 0.2):
    df = pd.read_csv(input_path)

    # Убираем пробелы в названиях колонок
    df.columns = [col.strip() for col in df.columns]

    # Переименовываем таргет
    df = df.rename(columns={"default.payment.next.month": "def_pay"})

    # Разделяем X / y
    y = df["def_pay"]
    X = df.drop(columns=["def_pay"])

    # Train / test split
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=test_size, random_state=42, stratify=y
    )

    # Сохраняем
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    X_train.to_csv(output_path / "X_train.csv", index=False)
    X_test.to_csv(output_path / "X_test.csv", index=False)
    y_train.to_csv(output_path / "y_train.csv", index=False)
    y_test.to_csv(output_path / "y_test.csv", index=False)


if __name__ == "__main__":
    prepare_dataset(sys.argv[1], sys.argv[2])
