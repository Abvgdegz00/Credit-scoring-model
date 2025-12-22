import mlflow
import mlflow.sklearn
import pandas as pd
import joblib
import json
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt

from sklearn.metrics import (
    roc_auc_score,
    f1_score,
    precision_score,
    recall_score,
    roc_curve,
)
from sklearn.model_selection import RandomizedSearchCV
from scipy.stats import randint, uniform
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from xgboost import XGBClassifier

from src.create_models.pipeline import create_pipeline
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.parent.parent
DATA_DIR = PROJECT_ROOT / "data" / "processed"
MODELS_DIR = PROJECT_ROOT / "models"
MODELS_DIR.mkdir(exist_ok=True)

# Загружаем данные
X_train = pd.read_csv(DATA_DIR / "X_train.csv")
y_train = pd.read_csv(DATA_DIR / "y_train.csv").values.ravel()
X_test = pd.read_csv(DATA_DIR / "X_test.csv")
y_test = pd.read_csv(DATA_DIR / "y_test.csv").values.ravel()

print("Train shape:", X_train.shape)
print("Test shape:", X_test.shape)

# Инициализируем MLflow
mlflow.set_tracking_uri("file:///" + str(PROJECT_ROOT / "mlruns"))
mlflow.set_experiment("Credit_Default_Prediction")

# Пространства гиперпараметров для разных моделей
search_spaces = {
    "GradientBoosting": {
        "model": GradientBoostingClassifier(random_state=42),
        "params": {
            "classifier__n_estimators": randint(100, 300),
            "classifier__learning_rate": uniform(0.01, 0.1),
            "classifier__max_depth": randint(3, 6),
            "classifier__subsample": uniform(0.7, 0.3),
            "classifier__min_samples_split": randint(2, 10),
            "classifier__min_samples_leaf": randint(1, 5),
        },
    },
    "RandomForest": {
        "model": RandomForestClassifier(random_state=42, n_jobs=-1),
        "params": {
            "classifier__n_estimators": randint(100, 400),
            "classifier__max_depth": randint(5, 20),
            "classifier__min_samples_split": randint(2, 10),
            "classifier__min_samples_leaf": randint(1, 5),
            "classifier__max_features": ["sqrt", "log2", None],
        },
    },
    "XGBoost": {
        "model": XGBClassifier(
            random_state=42,
            eval_metric="logloss",
            use_label_encoder=False,
            n_jobs=-1,
        ),
        "params": {
            "classifier__n_estimators": randint(100, 300),
            "classifier__max_depth": randint(3, 10),
            "classifier__learning_rate": uniform(0.01, 0.2),
            "classifier__subsample": uniform(0.6, 0.4),
            "classifier__colsample_bytree": uniform(0.6, 0.4),
            "classifier__gamma": uniform(0, 5),
            "classifier__reg_alpha": uniform(0, 1),
            "classifier__reg_lambda": uniform(0, 1),
        },
    },
}

results_summary = {}
best_auc = 0.0
best_model = None
best_name = None

# Последовательно обучаем несколько моделей
for model_name, cfg in search_spaces.items():
    with mlflow.start_run(run_name=model_name):
        print(f"\nTraining {model_name}")

        pipeline = create_pipeline(cfg["model"])

        search = RandomizedSearchCV(
            estimator=pipeline,
            param_distributions=cfg["params"],
            n_iter=20,
            scoring="roc_auc",
            cv=3,
            random_state=42,
            n_jobs=-1,
            verbose=1,
        )

        search.fit(X_train, y_train)
        model = search.best_estimator_

        y_pred = model.predict(X_test)
        y_proba = model.predict_proba(X_test)[:, 1]

        auc = roc_auc_score(y_test, y_proba)
        f1 = f1_score(y_test, y_pred)
        precision = precision_score(y_test, y_pred)
        recall = recall_score(y_test, y_pred)

        mlflow.log_params(search.best_params_)
        mlflow.log_metric("test_auc", auc)
        mlflow.log_metric("test_f1", f1)
        mlflow.log_metric("test_precision", precision)
        mlflow.log_metric("test_recall", recall)

        # ROC-кривая
        fpr, tpr, _ = roc_curve(y_test, y_proba)
        plt.figure()
        plt.plot(fpr, tpr, label=f"AUC={auc:.4f}")
        plt.plot([0, 1], [0, 1], "k--")
        plt.xlabel("False Positive Rate")
        plt.ylabel("True Positive Rate")
        plt.title(f"ROC Curve - {model_name}")
        plt.legend()

        roc_path = MODELS_DIR / f"roc_{model_name}.png"
        plt.savefig(roc_path)
        plt.close()

        mlflow.log_artifact(str(roc_path))

        results_summary[model_name] = {
            "auc": auc,
            "f1": f1,
            "precision": precision,
            "recall": recall,
        }

        if auc > best_auc:
            best_auc = auc
            best_model = model
            best_name = model_name

        print(f"{model_name} AUC: {auc:.4f}")

# Сохраняем лучшую модель
joblib.dump(best_model, MODELS_DIR / "credit_default_model.pkl")

with mlflow.start_run(run_name="BEST_MODEL"):
    mlflow.log_metric("best_auc", best_auc)
    mlflow.sklearn.log_model(best_model, "best_model", input_example=X_train.head(3))

with open(PROJECT_ROOT / "metrics_summary.json", "w") as f:
    json.dump(results_summary, f, indent=2)

print(f"\nBest model: {best_name}, AUC={best_auc:.4f}")
