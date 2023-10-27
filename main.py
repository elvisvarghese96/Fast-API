from fastapi import FastAPI, Depends
from fastapi.params import Body
from psycopg2.extras import RealDictCursor
import time
from sqlalchemy.orm import Session
from database import engine, SessionLocal, get_db 
import models, schemas
from passlib.context import CryptContext
from routers import post, user, auth, vote

context = CryptContext(schemes=["bcrypt"], deprecated = "auto")

models.Base.metadata.create_all(bind = engine)

app = FastAPI()


# class Post(BaseModel):
#     title: str
#     content: str
#    # name: str

# Firstposts = [{"title": "frst first is this","content":"content is this", "id":1},
#                { "title": "second content","content":"content is 2nd", "id":2 }]

# def findmyposts(id):
#     for pt in Firstposts:
#         if pt["id"] == id:
#             return pt

# def deletePost(id):
#     for i,item in enumerate(Firstposts):
#         if item["id"] == id:
#             return i


app.include_router(post.router)                     # path file name from other file using router
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(vote.router)


@app.get("/")                                   #decorator with root path
def root():
    return {"message": "First API project!???"}


@app.get("/sqlalchemy")
def testing_sqlalchemy(db: Session = Depends(get_db)):
    return {"status": "successfull"}

# @app.get("/getpost", status_code=status.HTTP_201_CREATED, response_model = List[schemas.response] )
# def getpost(db: Session = Depends(get_db)):
    
#     # thePost = cursor.execute("""SELECT * FROM "Post" """)
#     # postsCollect = cursor.fetchall()
#     #print(postsCollect)
#     #print(thePost)
#     postsCollectn = db.query(models.Post).all()
#     return postsCollectn
    


# @app.post("/newpost", status_code=status.HTTP_201_CREATED, response_model = schemas.response )
# def createpost(post: schemas.postCreate, db: Session = Depends(get_db)):        #Post is from class declred post above   #print(post.title)                                                                 
    
#     # cursor.execute("""INSERT INTO "Post" (title,content) VALUES (%s,%s) RETURNING * """,(post.title, post.content))
#     # insertPost = cursor.fetchone()
#     # conn.commit()
#     # postDict = post.dict()
#     # postDict["id"] = random.randrange(0, 10000)
#     # Firstposts.append(postDict)
#     #return {"new_post": f"title {load['title']} content: {load['content']}"} 
#     insertPost = models.Post(**post.dict())
#     db.add(insertPost)
#     db.commit()
#     db.refresh(insertPost)
#     return insertPost

# @app.get("/getpost/lastpost")
# def latest():
#     latestpost = Firstposts[len(Firstposts)-1]
#     return {"latest": latestpost}

# @app.get("/post/{id}", status_code = status.HTTP_201_CREATED, response_model = schemas.response)                   #decorater func
# def get_post_id(id: str, db: Session = Depends(get_db)):

#     #print(id)
#     # cursor.execute(""" SELECT * FROM "Post" WHERE id = %s returning * """, (str(id)))
#     # p = cursor.fetchone()
#     #post = findmyposts(id)                  #picks id from the func findmypost and the line hashed bcoz the data is fetched from db now 
#     post = db.query(models.Post).filter(models.Post.id == id).first()
    
#     if not post:
#         raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail= f"the post with {id} does not exist")
#     return post


# @app.delete("/delete/{id}", status_code = status.HTTP_204_NO_CONTENT)
# def delete(id: int, db: Session = Depends(get_db)):
#     #index = deletePost(id)
#     # cursor.execute("""DELETE FROM "Post" WHERE id= %s returning * """, (str(id)))
#     # deletePost = cursor.fetchone()
#     # conn.commit()
#     #Firstposts.pop(index)
    
#     post = db.query(models.Post).filter(models.Post.id == id)
#     #post = post_old.first()
#     if post.first() == None:
#         raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail= f"the post with {id} does not exist")
#     post.delete(synchronize_session = False)
#     db.commit()
#     return { "post_update": post.first() }


# @app.put("/updatepost/{id}", status_code = status.HTTP_201_CREATED, response_model = schemas.response)
# def post_updated( id:int, updated: schemas.postCreate, db: Session = Depends(get_db)):
#     #index = findmyposts(id)
#     #cursor.execute("""UPDATE "Post" set title=%s, content=%s WHERE id = %s RETURNING * """, (post.title, post.content, str(id)))
#     # try:
#     #     new_update = """UPDATE "Post" set title=%s, content=%s where id=%s RETURNING * """
#     #     cursor.execute(new_update,(post.title, post.content, str(id)))
#     # except Exception as error:
#     #     print(error)

#         #raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail= f"the error is {error}")
#     # new_update = cursor.fetchone()
#     # conn.commit()
#     # if new_update is None:
#     #   raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail= f"the post with {id} not exist")
#     #postupd = post.dict()
#     # postupd["id"] = id
#     # Firstposts[index] = postupd
#     #return {"postDetail" : new_update}

#     post_q = db.query(models.Post).filter(models.Post.id == id)
#     postupdate = post_q.first()
#     if postupdate == None:
#         raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail= f"the post with {id} does not exist")
#     post_q.update(updated.dict(), synchronize_session = False)
#     db.commit()
#     return post_q.first()


# @app.post("/userCreate", status_code = status.HTTP_201_CREATED)
# def post_updated(adduser : schemas.new_users, db: Session = Depends(get_db)):
    
#     hashedpassw = context.hash(adduser.password)
#     adduser.password = hashedpassw

#     insertedUser = models.User(**adduser.dict())
#     db.add(insertedUser)
#     db.commit()
#     db.refresh(insertedUser)
#     return insertedUser

















