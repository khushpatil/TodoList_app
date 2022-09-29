from fastapi import APIRouter, Depends, HTTPException
from .. import models,schema
from ..database import get_db
from sqlalchemy.orm import Session
from typing import List
from ..utils import hash_password

router = APIRouter(tags=['Users'])

@router.get("/users", response_model=List[schema.UserResponse])
def get_users(db : Session = Depends(get_db)):

    users = db.query(models.User).all()
    return users

@router.post("/users", response_model=schema.UserResponse, status_code=201)
def create_user(user: schema.User, db : Session = Depends(get_db)):

    user.Password = hash_password(user.Password)

    new_user = models.User(**user.dict())

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user

@router.delete("/users/{id}", status_code=204)
def delete_user(id: int, db: Session = Depends(get_db)):

    user = db.query(models.User).filter(models.User.User_ID == id)

    if not user.first():
        raise HTTPException(status_code=404, detail="The requested user doesn't exist")

    user.delete(synchronize_session=False)      
    db.commit()

    return {"message": "The resource has been deleted successfully"}