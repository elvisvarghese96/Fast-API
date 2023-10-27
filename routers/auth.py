from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
import models, schemas, utils
from database import engine, SessionLocal, get_db

router =  APIRouter(tags=['Authentication'])

@router.post('/login', status_code = status.HTTP_201_CREATED)
def login(loginDetails : schemas.login, db: Session = Depends(get_db)):
    userLogin = db.query(models.User).filter(models.User.email == loginDetails.email).first()
    #login = userLogin.first()
    if not login:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail= f"email/password wrong")
    
    if not utils.verifyPassword(loginDetails.password, userLogin.password):
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail= f"email/password wrong")
    
    return {"token": "Your credentials are verfied"}


