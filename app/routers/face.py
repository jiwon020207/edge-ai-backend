from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
import app.schemas as schemas, app.crud as crud
from app.database import get_db
from app.routers.auth import get_current_user

router = APIRouter()

@router.get("/api/v1/faces/", response_model=list[schemas.FaceOut])
def list_faces(current_user=Depends(get_current_user), db=Depends(get_db)):
    return crud.get_faces_by_user(db, current_user.id)

@router.post("/api/v1/faces/", response_model=schemas.FaceOut, status_code=status.HTTP_201_CREATED)
def add_face(face_in: schemas.FaceCreate, current_user=Depends(get_current_user), db=Depends(get_db)):
    return crud.create_face(db, current_user.id, face_in)

@router.delete("/api/v1/faces/{face_id}", status_code=status.HTTP_204_NO_CONTENT)
def remove_face(face_id: int, current_user=Depends(get_current_user), db=Depends(get_db)):
    if not any(f.id == face_id for f in crud.get_faces_by_user(db, current_user.id)):
        raise HTTPException(404, "해당 얼굴이 없습니다")
    crud.delete_face(db, face_id)
