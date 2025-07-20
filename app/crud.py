from sqlalchemy.orm import Session
from passlib.context import CryptContext
import app.models as models
import app.schemas as schemas

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()

def create_user(db: Session, user: schemas.UserCreate):
    hashed = pwd_context.hash(user.password)
    db_user = models.User(email=user.email, hashed_password=hashed)
    db.add(db_user); db.commit(); db.refresh(db_user)
    return db_user

def get_faces_by_user(db: Session, user_id: int):
    return db.query(models.Face).filter(models.Face.user_id == user_id).all()

def create_face(db: Session, user_id: int, face: schemas.FaceCreate):
    db_face = models.Face(user_id=user_id, label=face.label, image_url=face.image_url)
    db.add(db_face); db.commit(); db.refresh(db_face)
    return db_face

def delete_face(db: Session, face_id: int):
    face = db.query(models.Face).get(face_id)
    if face:
        db.delete(face); db.commit()

def get_protections_by_user(db: Session, user_id: int):
    return db.query(models.ProtectionSetting).filter(models.ProtectionSetting.user_id == user_id).all()

def create_protection(db: Session, user_id: int, prot: schemas.ProtectionCreate):
    db_prot = models.ProtectionSetting(user_id=user_id, url_pattern=prot.url_pattern, mode=prot.mode)
    db.add(db_prot); db.commit(); db.refresh(db_prot)
    return db_prot

def delete_protection(db: Session, prot_id: int):
    prot = db.query(models.ProtectionSetting).get(prot_id)
    if prot:
        db.delete(prot); db.commit()
