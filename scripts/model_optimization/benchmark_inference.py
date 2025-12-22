import torch
import onnxruntime as ort
import numpy as np
import time
from src.create_models.nn_model import CreditNN
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.parent.parent
MODEL_DIR = PROJECT_ROOT / "models"

# PyTorch бенчмарк
model = CreditNN(input_dim=23)
model.load_state_dict(torch.load(MODEL_DIR / "credit_nn_model.pth"))
model.eval()
x = torch.randn(1000, 23)

start = time.time()
with torch.no_grad():
    for _ in range(10):
        _ = model(x)
torch_time = time.time() - start

# ONNX бенчмарк
ort_session = ort.InferenceSession(str(MODEL_DIR / "credit_nn_model.onnx"))
x_np = x.numpy()
start = time.time()
for _ in range(10):
    _ = ort_session.run(None, {"input": x_np})
onnx_time = time.time() - start

# Квантизированная ONNX бенчмарк
ort_session_q = ort.InferenceSession(str(MODEL_DIR / "credit_nn_model_quant.onnx"))
start = time.time()
for _ in range(10):
    _ = ort_session_q.run(None, {"input": x_np})
quant_time = time.time() - start

print(f"PyTorch inference time: {torch_time:.4f}s")
print(f"ONNX inference time: {onnx_time:.4f}s")
print(f"Quantized ONNX inference time: {quant_time:.4f}s")
