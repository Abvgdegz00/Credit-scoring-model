from sklearn.pipeline import Pipeline
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import StandardScaler


def create_pipeline(gb_params=None):
    if gb_params is None:
        gb_params = {
            'n_estimators': 175,
            'learning_rate': 0.03834279478157687,
            'max_depth': 5,
            'min_samples_split': 9,
            'min_samples_leaf': 3,
            'subsample': 0.6796169854953065,
            'max_features': None,
            'random_state': 42
        }

    # Определяем числовые и категориальные признаки
    numeric_features = ['LIMIT_BAL', 'AGE', 'BILL_AMT1', 'BILL_AMT2', 'BILL_AMT3',
                        'BILL_AMT4', 'BILL_AMT5', 'BILL_AMT6', 'PAY_AMT1', 'PAY_AMT2',
                        'PAY_AMT3', 'PAY_AMT4', 'PAY_AMT5', 'PAY_AMT6']

    categorical_features = ['SEX', 'EDUCATION', 'MARRIAGE', 'PAY_0', 'PAY_2', 'PAY_3',
                            'PAY_4', 'PAY_5', 'PAY_6']

    # Создаем препроцессор
    preprocessor = ColumnTransformer(
        transformers=[
            ('num', StandardScaler(), numeric_features),
            ('cat', 'passthrough', categorical_features)
        ]
    )

    # Создаем пайплайн
    pipeline = Pipeline([
        ('preprocessor', preprocessor),
        ('classifier', GradientBoostingClassifier(**gb_params))
    ])

    return pipeline
