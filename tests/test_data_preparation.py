import pandas as pd
from src.data.make_dataset import prepare_dataset


def test_prepare_dataset(tmp_path):
    input_csv = tmp_path / "input.csv"
    df = pd.DataFrame(
        {
            "ID": [1, 2, 3, 4],
            "LIMIT_BAL": [1000, 2000, 1500, 2500],
            "AGE": [25, 35, 30, 40],
            "default.payment.next.month": [0, 0, 1, 1],
        }
    )
    df.to_csv(input_csv, index=False)

    # передаем test_size=0.5 для мини-даты
    prepare_dataset(str(input_csv), str(tmp_path), test_size=0.5)

    # Проверяем что файлы созданы
    assert (tmp_path / "X_train.csv").exists()
    assert (tmp_path / "X_test.csv").exists()
    assert (tmp_path / "y_train.csv").exists()
    assert (tmp_path / "y_test.csv").exists()
