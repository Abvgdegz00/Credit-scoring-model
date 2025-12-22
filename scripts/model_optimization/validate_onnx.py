import torch
import onnx
import onnxruntime as ort
import numpy as np
from src.create_models.nn_model import CreditNN
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.parent.parent
MODEL_DIR = PROJECT_ROOT / "models"

# Загрузка обычной модели
model = CreditNN(input_dim=23)
model.load_state_dict(torch.load(MODEL_DIR / "credit_nn_model.pth"))
model.eval()

# Загрузка ONNX модели
onnx_model_path = MODEL_DIR / "credit_nn_model.onnx"
ort_session = ort.InferenceSession(str(onnx_model_path))

# Тестовый ввод
x = torch.randn(5, 23)

# Инференс обычной модели
torch_out = model(x).detach().numpy()

# Инференс ONNX
ort_out = ort_session.run(None, {"input": x.numpy()})[0]

# Сравнение результатов
np.testing.assert_allclose(torch_out, ort_out, rtol=1e-03, atol=1e-05)
print("ONNX модель совпадает с PyTorch моделью")
