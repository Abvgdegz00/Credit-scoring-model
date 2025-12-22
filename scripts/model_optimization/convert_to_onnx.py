import torch
from src.create_models.nn_model import CreditNN
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.parent.parent
MODEL_DIR = PROJECT_ROOT / "models"

# Загрузка Pytorch модели
model = CreditNN(input_dim=23)
model.load_state_dict(torch.load(MODEL_DIR / "credit_nn_model.pth"))
model.eval()

dummy_input = torch.randn(1, 23)

# Экспорт в ONNX
onnx_path = MODEL_DIR / "credit_nn_model.onnx"
torch.onnx.export(
    model,
    dummy_input,
    onnx_path,
    input_names=["input"],
    output_names=["output"],
    dynamic_axes={"input": {0: "batch_size"}, "output": {0: "batch_size"}},
    opset_version=13
)

print(f"ONNX модель сохранена: {onnx_path}")
