# app/routers/inference.py
from fastapi import APIRouter, Depends, HTTPException
import app.schemas as schemas
from app.routers.auth import get_current_user
from app.database import get_db
from sqlalchemy.orm import Session
import onnxruntime as ort
import numpy as np

router = APIRouter(prefix="/api/v1/inference", tags=["inference"])

# 애플리케이션 시작 시 최적화된 모델 로드 (예시)
session = ort.InferenceSession("models/latest_model.onnx")

@router.post("/", response_model=schemas.InferenceOut)
def run_inference(data: schemas.InferenceIn,
                  current_user=Depends(get_current_user),
                  db: Session = Depends(get_db)):
    # 1) 입력 전처리: 좌표·URL → 모델 입력 텐서
    input_tensor = np.array([[data.x_coord, data.y_coord]], dtype=np.float32)
    input_name  = session.get_inputs()[0].name

    # 2) 추론 실행
    outputs = session.run(None, {input_name: input_tensor})
    score   = float(outputs[0][0])  # 예: [0]=눈 감지 확률

    # 3) 결과 해석
    if score > 0.5:
        action, reason = "alert", "user is not looking"
    else:
        action, reason = "ok", "user is looking"

    return schemas.InferenceOut(action=action, reason=reason)
