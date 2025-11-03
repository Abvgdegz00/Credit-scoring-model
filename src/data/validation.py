import great_expectations as ge
from great_expectations.core.expectation_configuration import ExpectationConfiguration
import pandas as pd
from pathlib import Path


# Создаем набор правил для валидации данных
def create_expectation_suite():
    expectation_suite_name = "credit_default_suite"

    context = ge.get_context()

    try:
        suite = context.get_expectation_suite(expectation_suite_name)
        suite.expectations = []
    except Exception as e:
        print(f"GE context error: {e}")
        suite = context.create_expectation_suite(expectation_suite_name)

    expectations = [
        ExpectationConfiguration(
            expectation_type="expect_table_columns_to_match_ordered_list",
            kwargs={
                "column_list": [
                    "ID",
                    "LIMIT_BAL",
                    "SEX",
                    "EDUCATION",
                    "MARRIAGE",
                    "AGE",
                    "PAY_0",
                    "PAY_2",
                    "PAY_3",
                    "PAY_4",
                    "PAY_5",
                    "PAY_6",
                    "BILL_AMT1",
                    "BILL_AMT2",
                    "BILL_AMT3",
                    "BILL_AMT4",
                    "BILL_AMT5",
                    "BILL_AMT6",
                    "PAY_AMT1",
                    "PAY_AMT2",
                    "PAY_AMT3",
                    "PAY_AMT4",
                    "PAY_AMT5",
                    "PAY_AMT6",
                    "default.payment.next.month",
                ]
            },
        ),
        ExpectationConfiguration(
            expectation_type="expect_column_values_to_not_be_null",
            kwargs={"column": "LIMIT_BAL"},
        ),
        ExpectationConfiguration(
            expectation_type="expect_column_values_to_be_between",
            kwargs={"column": "AGE", "min_value": 18, "max_value": 100},
        ),
        ExpectationConfiguration(
            expectation_type="expect_column_values_to_be_in_set",
            kwargs={"column": "SEX", "value_set": [1, 2]},
        ),
        ExpectationConfiguration(
            expectation_type="expect_column_values_to_be_in_set",
            kwargs={"column": "default.payment.next.month", "value_set": [0, 1]},
        ),
    ]

    for expectation in expectations:
        suite.add_expectation(expectation_configuration=expectation)

    context.save_expectation_suite(suite)
    return suite


def validate_data(df: pd.DataFrame, suite_name: str = "credit_default_suite"):

    df_ge = ge.from_pandas(df)

    context = ge.get_context()
    suite = context.get_expectation_suite(suite_name)

    results = df_ge.validate(expectation_suite=suite)

    if not results.success:
        print("Валидация не пройдена! Ошибки:")
        for result in results.results:
            if not result.success:
                print(
                    f" - {result.expectation_config.expectation_type}: {result.result}"
                )
        raise ValueError("Данные не прошли валидацию")
    return True


if __name__ == "__main__":
    test_df = pd.read_csv(
        Path(__file__).parent.parent.parent / "data" / "processed" / "X_train.csv"
    )
    create_expectation_suite()
    validate_data(test_df)
