from fastapi import HTTPException, Depends, APIRouter, Response
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from .. import database,schema,models,utils,auth2

router = APIRouter(tags=['Authentication'])

@router.post("/login")
def login(user_credentials: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(database.get_db)):

    user = db.query(models.User).filter(models.User.Email == user_credentials.username).first()

    if not user:
        raise HTTPException(status_code=404, detail="Invalid Credentials")

    if not utils.verify(user_credentials.password, user.Password):
        raise HTTPException(status_code=404, detail="Invalid Credentials")

    access_token = auth2.create_access_token(data= {"User_ID": user.User_ID})

    return {"access_token": access_token, "token_type": "bearer"}

