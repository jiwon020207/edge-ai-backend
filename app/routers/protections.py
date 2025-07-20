from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
import app.schemas as schemas, app.crud as crud
from app.database import get_db
from app.routers.auth import get_current_user

router = APIRouter()

@router.get("/api/v1/protections/", response_model=list[schemas.ProtectionOut])
def list_protections(current_user=Depends(get_current_user), db=Depends(get_db)):
    return crud.get_protections_by_user(db, current_user.id)

@router.post("/api/v1/protections/", response_model=schemas.ProtectionOut, status_code=status.HTTP_201_CREATED)
def add_protection(prot_in: schemas.ProtectionCreate, current_user=Depends(get_current_user), db=Depends(get_db)):
    return crud.create_protection(db, current_user.id, prot_in)

@router.delete("/api/v1/protections/{prot_id}", status_code=status.HTTP_204_NO_CONTENT)
def remove_protection(prot_id: int, current_user=Depends(get_current_user), db=Depends(get_db)):
    if not any(p.id == prot_id for p in crud.get_protections_by_user(db, current_user.id)):
        raise HTTPException(404, "해당 설정이 없습니다")
    crud.delete_protection(db, prot_id)
