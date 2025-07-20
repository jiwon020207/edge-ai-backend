from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
import app.crud as crud, app.schemas as schemas
from app.database import get_db
from app.routers.auth import get_current_user

router = APIRouter(prefix="/api/v1/models", tags=["models"])

@router.post("/train", response_model=schemas.TrainingJobOut)
def start_training(db: Session = Depends(get_db),
                   current_user=Depends(get_current_user)):
    return crud.create_training_job(db, current_user.id)

@router.get("/train/{job_id}", response_model=schemas.TrainingJobOut)
def get_training_status(job_id: int, db: Session = Depends(get_db),
                        current_user=Depends(get_current_user)):
    job = crud.get_training_job(db, job_id)
    if not job or job.user_id != current_user.id:
        raise HTTPException(404, "Job not found")
    return job

@router.post("/optimize/{job_id}", response_model=schemas.OptimizeOut)
def optimize_model(job_id: int, db: Session = Depends(get_db),
                   current_user=Depends(get_current_user)):
    # TODO: ONNX 변환 로직 후 실제 경로 지정
    path = f"/models/{job_id}.onnx"
    return crud.create_optimized_model(db, job_id, path)
