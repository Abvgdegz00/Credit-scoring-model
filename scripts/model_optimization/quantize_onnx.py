import onnx
from onnxruntime.quantization import quantize_dynamic, QuantType
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.parent.parent
MODEL_DIR = PROJECT_ROOT / "models"

onnx_model_path = MODEL_DIR / "credit_nn_model.onnx"
quant_model_path = MODEL_DIR / "credit_nn_model_quant.onnx"

quantize_dynamic(
    model_input=str(onnx_model_path),
    model_output=str(quant_model_path),
    weight_type=QuantType.QInt8
)

print(f"Квантизированная модель сохранена {quant_model_path}")
