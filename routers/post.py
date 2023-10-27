from typing import List, Optional
import models, schemas
from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from database import engine, SessionLocal, get_db 
from sqlalchemy.orm import Session
from passlib.context import CryptContext
context = CryptContext(schemes=["bcrypt"], deprecated = "auto")

router = APIRouter()


@router.get("/getpost", status_code=status.HTTP_201_CREATED, response_model = List[schemas.outpost] )
def getpost(db: Session = Depends(get_db), limit:int = 10, search: Optional[str] = ""):
    
    # thePost = cursor.execute("""SELECT * FROM "Post" """)
    # postsCollect = cursor.fetchall()
    #print(postsCollect)
    #print(thePost)
    #print(limit)
    #postsCollectn = db.query(models.Post).filter(models.Post.title.contains(search)).limit(limit).all()
    
    postsCollectn = db.query(models.Post).join(models.User, models.User.id == models.Post.id, isouter = True).group_by(models.Post.id).filter(models.Post.title.contains(search)).limit(limit).all()
    
    return postsCollectn


@router.post("/newpost", status_code=status.HTTP_201_CREATED, response_model = schemas.response )
def createpost(post: schemas.postCreate, db: Session = Depends(get_db)):                                            #Post is from class declred post above   #print(post.title)                                                                 
    # cursor.execute("""INSERT INTO "Post" (title,content) VALUES (%s,%s) RETURNING * """,(post.title, post.content))
    # insertPost = cursor.fetchone()
    # conn.commit()
    # postDict = post.dict()
    # postDict["id"] = random.randrange(0, 10000)
    # Firstposts.append(postDict)
    #return {"new_post": f"title {load['title']} content: {load['content']}"}
    
    post.owner_id = 52
    insertPost = models.Post(**post.dict())
    db.add(insertPost)
    db.commit()
    db.refresh(insertPost)
    return insertPost
 

@router.get("/post/{id}", status_code = status.HTTP_201_CREATED, response_model = schemas.response)                   #decorater func
def get_post_id(id: str, db: Session = Depends(get_db)):

    #print(id)
    # cursor.execute(""" SELECT * FROM "Post" WHERE id = %s returning * """, (str(id)))
    # p = cursor.fetchone()
    #post = findmyposts(id)                  #picks id from the func findmypost and the line hashed bcoz the data is fetched from db now 
    post = db.query(models.Post).filter(models.Post.id == id).first()
    if not post:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail= f"the post with {id} does not exist")
    return post


@router.delete("/delete/{id}", status_code = status.HTTP_204_NO_CONTENT)
def delete(id: int, db: Session = Depends(get_db)):
    #index = deletePost(id)
    # cursor.execute("""DELETE FROM "Post" WHERE id= %s returning * """, (str(id)))
    # deletePost = cursor.fetchone()
    # conn.commit()
    #Firstposts.pop(index)
    
    post = db.query(models.Post).filter(models.Post.id == id)
    #post = post_old.first()
    if post.first() == None:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail= f"the post with {id} does not exist")
    post.delete(synchronize_session = False)
    db.commit()
    return { "post_update": post.first() }


@router.put("/updatepost/{id}", status_code = status.HTTP_201_CREATED, response_model = schemas.response)
def post_updated( id:int, updated: schemas.postCreate, db: Session = Depends(get_db)):
    #index = findmyposts(id)
    #cursor.execute("""UPDATE "Post" set title=%s, content=%s WHERE id = %s RETURNING * """, (post.title, post.content, str(id)))
    # try:
    #     new_update = """UPDATE "Post" set title=%s, content=%s where id=%s RETURNING * """
    #     cursor.execute(new_update,(post.title, post.content, str(id)))
    # except Exception as error:
    #     print(error)

        #raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail= f"the error is {error}")
    # new_update = cursor.fetchone()
    # conn.commit()
    # if new_update is None:
    #   raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail= f"the post with {id} not exist")
    #postupd = post.dict()
    # postupd["id"] = id
    # Firstposts[index] = postupd
    #return {"postDetail" : new_update}

    post_q = db.query(models.Post).filter(models.Post.id == id)
    postupdate = post_q.first()
    if postupdate == None:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail= f"the post with {id} does not exist")
    post_q.update(updated.dict(), synchronize_session = False)
    db.commit()
    return post_q.first()



