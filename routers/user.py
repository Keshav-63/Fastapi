from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from database import get_db
import models, schemas, utlis

router = APIRouter(
    prefix="/users",
    tags= ['Users']
)

# Users

@router.post("/", status_code = status.HTTP_201_CREATED, response_model=schemas.UserOut)
def creat_users(create_user: schemas.UserCreate, db: Session = Depends(get_db)):
    user = models.User(**create_user.dict())
    user.password = utlis.hash(create_user.password)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

@router.get("/{id}", response_model=schemas.UserOut)
def get_user(id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"user with {id} not found")
    
    return user
