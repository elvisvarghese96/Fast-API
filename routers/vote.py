from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from database import engine, SessionLocal, get_db 
import models, schemas
from sqlalchemy.orm import Session

router = APIRouter()

@router.post("/vote", status_code = status.HTTP_201_CREATED )                   #decorater func
def voting(vote:schemas.vote, user: schemas.user ,db: Session = Depends(get_db)):
    
    post_check = db.query(models.Post).filter(models.Post.id == vote.postID).first()
    
    if not post_check:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"the post with {vote.postID} not exist")
    
    voting_query = db.query(models.Vote).filter(models.Vote.postId == vote.postid, models.Vote.userId == vote.userid)
    vote_valid = voting_query.first()

    #return vote_valid
    if (vote.dir == 1):
        if vote_valid:
            raise HTTPException(status_code = status.HTTP_409_CONFLICT, detail=f"the user already voted on the post {vote.postid}")
        newVote = models.Vote(post = vote.postid, userid = user.id)
        db.add(newVote)
        db.commit()
        return {"message":"post curently voted"}
        
    else:
        if not vote_valid:
            raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = f"Not voted")
    voting_query.delete(synchronize_session=False)
    db.commit()
    return {"message":"deleted vote"}







