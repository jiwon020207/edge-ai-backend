# app/routers/inference.py
import os
from fastapi import APIRouter, File, UploadFile, HTTPException
import numpy as np
import onnxruntime as ort
from PIL import Image

MODEL_PATH = "models/onnx/latest.onnx"
if not os.path.exists(MODEL_PATH):
    raise RuntimeError(f"ONNX not found: {MODEL_PATH}")

session = ort.InferenceSession(MODEL_PATH)
router = APIRouter(prefix="/api/v1/inference", tags=["inference"])

def preprocess_image(file: UploadFile) -> np.ndarray:
    img = Image.open(file.file).convert("RGB").resize((224,224))
    arr = np.array(img).astype(np.float32) / 255.0
    # 배치 차원 추가 (1,3,224,224)
    return np.transpose(arr, (2,0,1))[None, ...]

@router.post("/infer")
async def infer(file: UploadFile = File(...)):
    try:
        input_data = preprocess_image(file)
        outputs = session.run(None, {"input": input_data})
        return {"predictions": outputs[0].tolist()}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
