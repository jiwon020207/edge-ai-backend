from fastapi import APIRouter, Depends
import app.schemas as schemas
from app.routers.auth import get_current_user
from app.database import get_db
from sqlalchemy.orm import Session

router = APIRouter(prefix="/api/v1/inference", tags=["inference"])

@router.post("/", response_model=schemas.InferenceOut)
def run_inference(data: schemas.InferenceIn,
                  current_user=Depends(get_current_user),
                  db: Session = Depends(get_db)):
    # TODO: 실제 ML/NPU 호출 후 action, reason 반환
    return schemas.InferenceOut(action="blur", reason="placeholder")
