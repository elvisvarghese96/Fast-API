from pydantic import BaseModel, EmailStr
from datetime import datetime
from pydantic.types import conint


class PostBase(BaseModel):
    title: str
    content: str
    owner_id: int=None
    #owner: user 

class postCreate(PostBase):
    pass


class response(PostBase):
    id: int
    created_at: datetime
    owner_id: int
    
    class Config:
        orm_mode = True

class new_users(BaseModel):
    email: EmailStr
    password: str


class user(BaseModel):
    id: str
    email: EmailStr
    created_at: datetime

    class Config:
        orm_mode = True


class userCheck(new_users):
    pass

class outpost(BaseModel):
    post: response
    the_users: user
    class Config:
        orm_mode = True

class login(new_users):
    pass

class vote(BaseModel):
    userid: int
    postID: int
    dir: conint(le=1)



