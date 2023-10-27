from fastapi import FastAPI, Response, status
from passlib.context import CryptContext
from sqlalchemy.orm import Session
from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from passlib.context import CryptContext
import models, schemas
from database import get_db 

context = CryptContext(schemes=["bcrypt"], deprecated = "auto")

router = APIRouter()


@router.post("/userCreate", status_code = status.HTTP_201_CREATED)
def userCreate(adduser : schemas.new_users, db: Session = Depends(get_db)):
    
    username_exist = db.query(models.User).filter(models.User.email == adduser.email).first()

    if username_exist: 
        raise HTTPException(status_code = status.HTTP_400_BAD_REQUEST, detail= f"email/password already exist")
    
    hashedpassw = context.hash(adduser.password)
    adduser.password = hashedpassw
    insertedUser = models.User(**adduser.dict())
    db.add(insertedUser)
    db.commit()
    db.refresh(insertedUser)
    return insertedUser


@router.put("/updateUser/{id}", status_code = status.HTTP_201_CREATED, response_model = schemas.response)
def user_updated( id:int, updated: schemas.postCreate, db: Session = Depends(get_db)):

    userupdate = db.query(models.Post).filter(models.User.id == id)
    userNew = userupdate.first()
    if userNew == None:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail= f"the user with {id} does not exist")
    userupdate.update(updated.dict(), synchronize_session = False)
    db.commit()
    return userupdate.first()



