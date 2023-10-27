from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from sqlalchemy.sql.expression import null, text
from database import Base
from sqlalchemy.sql.sqltypes import TIMESTAMP

class Post(Base):
    __tablename__ = "Post"
    
    id = Column(Integer, primary_key=True, index=True, nullable = False)
    title = Column(String, nullable=False)
    content = Column(String, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))
    owner_id = Column(Integer,ForeignKey("User.id", ondelete = "CASCADE"), nullable = False)
   # owner = relationship("User")

class User(Base):
    __tablename__ = "User"

    id = Column(Integer, primary_key=True, index=True, nullable = False)
    email = Column(String, nullable = False)
    password = Column(String, nullable = False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))

class Vote(Base):
    __tablename__ = "Vote"

    userId = Column(Integer,ForeignKey("User.id", ondelete = "CASCADE"), primary_key=True)
    postId = Column(Integer,ForeignKey("Post.id", ondelete = "CASCADE"), primary_key=True)
   















