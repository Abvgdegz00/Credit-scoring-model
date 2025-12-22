import pandas as pd
from evidently.dashboard import Dashboard
from evidently.dashboard.tabs import DataDriftTab, RegressionPerformanceTab
from evidently.model_profile import Profile
from evidently.model_profile.sections import DataDriftProfileSection

# Параметры
REFERENCE_DATA_PATH = "data/reference_data.csv"
CURRENT_DATA_PATH = "data/current_data.csv"
MODEL_PATH = "models/credit_default_model.pkl"
REPORT_PATH = "reports/drift_report.html"

# Загружаем данные
reference_data = pd.read_csv(REFERENCE_DATA_PATH)
current_data = pd.read_csv(CURRENT_DATA_PATH)

# Data drift профилирование
profile = Profile(sections=[DataDriftProfileSection()])
profile.calculate(reference_data, current_data)

# Генерация HTML отчета
dashboard = Dashboard(tabs=[DataDriftTab(), RegressionPerformanceTab()])
dashboard.calculate(reference_data, current_data)
dashboard.save(REPORT_PATH)

print(f"Drift отчет сохранен в: {REPORT_PATH}")
