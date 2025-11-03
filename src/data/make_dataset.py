import pandas as pd
import sys
from sklearn.model_selection import train_test_split
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent.parent))
from src.features.build_features import build_features


# Загружаем данные, убираем пробелы в названиях колонок и делим на train/test.
def prepare_dataset(input_path: str, output_dir: str):
    df = pd.read_csv(input_path)
    df.columns = [col.strip() for col in df.columns]

    df = build_features(df)

    y = df["def_pay"]
    X = df.drop("def_pay", axis=1)

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )

    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    X_train.to_csv(output_path / "X_train.csv", index=False)
    X_test.to_csv(output_path / "X_test.csv", index=False)
    y_train.to_csv(output_path / "y_train.csv", index=False)
    y_test.to_csv(output_path / "y_test.csv", index=False)


if __name__ == "__main__":
    import sys

    prepare_dataset(sys.argv[1], sys.argv[2])
