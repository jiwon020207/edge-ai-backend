# app/routers/models.py
from fastapi import APIRouter, Depends, BackgroundTasks, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db, SessionLocal
import app.crud as crud, app.schemas as schemas
from app.routers.auth import get_current_user
import subprocess, os

router = APIRouter(prefix="/api/v1/models", tags=["models"])

def run_training(job_id: int):
    db = SessionLocal()
    job = crud.get_training_job(db, job_id)
    crud.update_training_status(db, job, "running")
    try:
        # 예: python scripts/train.py --data data/processed --model-output models/{job_id}.pth
        subprocess.run([
            "python", "scripts/train.py",
            "--data-dir", "data/processed",
            "--output", f"models/{job_id}.pth"
        ], check=True)
        crud.update_training_status(db, job, "completed")
    except Exception:
        crud.update_training_status(db, job, "failed")
    finally:
        db.close()

@router.post("/train", response_model=schemas.TrainingJobOut)
def start_training(background_tasks: BackgroundTasks,
                   db: Session = Depends(get_db),
                   current_user=Depends(get_current_user)):
    job = crud.create_training_job(db, current_user.id)
    background_tasks.add_task(run_training, job.id)
    return job
