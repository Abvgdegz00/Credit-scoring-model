import mlflow
import mlflow.sklearn
import pandas as pd
import joblib
import json
import matplotlib.pyplot as plt
from sklearn.metrics import roc_auc_score, f1_score, precision_score, recall_score, roc_curve
from sklearn.model_selection import RandomizedSearchCV
from scipy.stats import randint, uniform
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from xgboost import XGBClassifier
from src.features.build_features import build_features
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.parent.parent
DATA_DIR = PROJECT_ROOT / 'data' / 'processed'
MODELS_DIR = PROJECT_ROOT / 'models'

# Загружаем данные
X_train = pd.read_csv(DATA_DIR / 'X_train.csv')
y_train = pd.read_csv(DATA_DIR / 'y_train.csv').values.ravel()
X_test = pd.read_csv(DATA_DIR / 'X_test.csv')
y_test = pd.read_csv(DATA_DIR / 'y_test.csv').values.ravel()

X_train = build_features(X_train)
X_test = build_features(X_test)

print("Размер тренировочных данных:", X_train.shape)
print("Размер тестовых данных:", X_test.shape)

# Настройка MLflow
mlflow.set_tracking_uri('file:///' + str(PROJECT_ROOT / 'mlruns'))
mlflow.set_experiment('Credit_Default_Prediction')

# Определяем модели и Randomized Search сетки
search_spaces = {
    "GradientBoosting": {
        "model": GradientBoostingClassifier(random_state=42),
        "params": {
            "n_estimators": randint(100, 300),
            "learning_rate": uniform(0.01, 0.1),
            "max_depth": randint(3, 6),
            "subsample": uniform(0.7, 0.3),
            "min_samples_split": randint(2, 10),
            "min_samples_leaf": randint(1, 5)
        }
    },
    "RandomForest": {
        "model": RandomForestClassifier(random_state=42, n_jobs=-1),
        "params": {
            "n_estimators": randint(100, 400),
            "max_depth": randint(5, 20),
            "min_samples_split": randint(2, 10),
            "min_samples_leaf": randint(1, 5),
            "max_features": ["sqrt", "log2", None]
        }
    },
    "XGBoost": {
        "model": XGBClassifier(use_label_encoder=False, eval_metric="logloss", random_state=42, n_jobs=-1),
        "params": {
            "n_estimators": randint(100, 300),
            "max_depth": randint(3, 10),
            "learning_rate": uniform(0.01, 0.2),
            "subsample": uniform(0.6, 0.4),
            "colsample_bytree": uniform(0.6, 0.4),
            "gamma": uniform(0, 5),
            "reg_alpha": uniform(0, 1),
            "reg_lambda": uniform(0, 1)
        }
    }
}

results_summary = {}

for model_name, cfg in search_spaces.items():
    with mlflow.start_run(run_name=model_name):
        print(f"\nПодбор гиперпараметров для {model_name}")

        search = RandomizedSearchCV(
            estimator=cfg["model"],
            param_distributions=cfg["params"],
            n_iter=20,          # количество случайных комбинаций
            scoring="roc_auc",
            cv=3,
            random_state=42,
            n_jobs=-1,
            verbose=2
        )

        search.fit(X_train, y_train)
        best_model = search.best_estimator_
        best_params = search.best_params_

        print(f"Лучшие параметры для {model_name}: {best_params}")
        mlflow.log_params(best_params)

        # Предсказания и метрики
        y_pred = best_model.predict(X_test)
        y_proba = best_model.predict_proba(X_test)[:, 1]

        auc = roc_auc_score(y_test, y_proba)
        f1 = f1_score(y_test, y_pred)
        precision = precision_score(y_test, y_pred)
        recall = recall_score(y_test, y_pred)

        mlflow.log_metric("test_auc", auc)
        mlflow.log_metric("test_f1", f1)
        mlflow.log_metric("test_precision", precision)
        mlflow.log_metric("test_recall", recall)

        # ROC-кривая
        fpr, tpr, _ = roc_curve(y_test, y_proba)
        plt.figure()
        plt.plot(fpr, tpr, label=f"AUC = {auc:.4f}")
        plt.plot([0, 1], [0, 1], 'k--')
        plt.xlabel("False Positive Rate")
        plt.ylabel("True Positive Rate")
        plt.title(f"ROC Curve - {model_name}")
        plt.legend(loc="lower right")
        MODELS_DIR.mkdir(exist_ok=True)
        roc_path = MODELS_DIR / f"roc_{model_name}.png"
        plt.savefig(roc_path)
        plt.close()
        mlflow.log_artifact(str(roc_path))

        # Сохраняем модель
        model_filename = MODELS_DIR / f"{model_name}_best_model.pkl"
        joblib.dump(best_model, model_filename)
        mlflow.sklearn.log_model(best_model, "model", input_example=X_train.head(3))

        results_summary[model_name] = {
            "best_params": best_params,
            "auc": auc,
            "f1": f1,
            "precision": precision,
            "recall": recall
        }

        print(f"{model_name} AUC: {auc:.4f}, F1: {f1:.4f}")

# Сохраняем summary
metrics_path = PROJECT_ROOT / "metrics_summary.json"
with open(metrics_path, "w") as f:
    json.dump(results_summary, f, indent=2)

print(f"\nВсе метрики и параметры сохранены в {metrics_path}")
