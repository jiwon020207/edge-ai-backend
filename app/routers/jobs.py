from fastapi import APIRouter, BackgroundTasks
import app.schemas as schemas

router = APIRouter(prefix="/api/v1/jobs", tags=["jobs"])

def run_preprocessing():
    # TODO: 실제 전처리 로직 구현
    pass

@router.post("/preprocess", response_model=schemas.JobOut)
def preprocess_data(background_tasks: BackgroundTasks):
    background_tasks.add_task(run_preprocessing)
    return {"message": "Preprocessing started in background"}
