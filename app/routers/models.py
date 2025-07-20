# app/routers/models.py

from fastapi import APIRouter, Depends, BackgroundTasks, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db, SessionLocal
import app.crud as crud
import app.schemas as schemas
from app.routers.auth import get_current_user
import subprocess
import os

router = APIRouter(prefix="/api/v1/models", tags=["models"])

def run_training(job_id: int):
    """
    1) TrainingJob.status를 'running'으로 업데이트
    2) scripts/train.py 호출하여 실제 학습 수행
    3) 성공 시 'completed', 실패 시 'failed'로 상태 업데이트
    """
    db = SessionLocal()
    try:
        job = crud.get_training_job(db, job_id)
        crud.update_training_status(db, job, "running")

        # 학습 스크립트 호출 (경로·인자 변경 가능)
        os.makedirs("models", exist_ok=True)
        subprocess.run([
            "python", "scripts/train.py",
            "--data-dir", "data/processed",
            "--output",   f"models/{job_id}.pth"
        ], check=True)

        crud.update_training_status(db, job, "completed")
    except Exception as e:
        crud.update_training_status(db, job, "failed")
        # 필요시 로그 기록: print(e) 또는 logging.error(e)
    finally:
        db.close()

@router.post("/train", response_model=schemas.TrainingJobOut)
def start_training(
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    """
    1) DB에 TrainingJob(status='pending') 생성
    2) BackgroundTasks로 run_training(job_id) 실행
    """
    job = crud.create_training_job(db, current_user.id)
    background_tasks.add_task(run_training, job.id)
    return job

@router.get("/train/{job_id}", response_model=schemas.TrainingJobOut)
def get_training_status(
    job_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    """
    특정 job_id의 학습 상태 조회
    """
    job = crud.get_training_job(db, job_id)
    if not job or job.user_id != current_user.id:
        raise HTTPException(status_code=404, detail="Job not found")
    return job

@router.post("/optimize/{job_id}", response_model=schemas.OptimizeOut)
def optimize_model(
    job_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    """
    1) 해당 job이 completed인지 확인
    2) scripts/convert_to_onnx.py 호출하여 ONNX 변환
    3) OptimizedModel에 변환된 경로 저장 후 반환
    """
    job = crud.get_training_job(db, job_id)
    if not job or job.user_id != current_user.id:
        raise HTTPException(status_code=404, detail="Job not found")
    if job.status != "completed":
        raise HTTPException(status_code=400, detail="Training not completed yet")

    # ONNX 변환
    os.makedirs("models/onnx", exist_ok=True)
    onnx_path = f"models/onnx/{job_id}.onnx"
    subprocess.run([
        "python", "scripts/convert_to_onnx.py",
        "--input",  f"models/{job_id}.pth",
        "--output", onnx_path
    ], check=True)

    opt = crud.create_optimized_model(db, job_id, onnx_path)
    return opt
