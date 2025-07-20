# app/routers/inference.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
import app.schemas as schemas
from app.database import get_db
from app.routers.auth import get_current_user
import onnxruntime as ort
import numpy as np
import os

router = APIRouter(prefix="/api/v1/inference", tags=["inference"])

MODEL_PATH = "models/onnx/latest.onnx"
if not os.path.exists(MODEL_PATH):
    raise RuntimeError(f"ONNX not found: {MODEL_PATH}")
sess = ort.InferenceSession(MODEL_PATH)

@router.post("/", response_model=schemas.InferenceOut)
def inference(
    data: schemas.InferenceIn,
    user=Depends(get_current_user),
    db: Session=Depends(get_db)
):
    x = np.array([[data.x_coord, data.y_coord]], dtype=np.float32)
    name = sess.get_inputs()[0].name
    out  = sess.run(None, {name: x})[0][0][0]
    action = "alert" if out>0.5 else "ok"
    return schemas.InferenceOut(action=action, reason=f"score={out:.2f}")
