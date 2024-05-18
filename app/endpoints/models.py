from sqlalchemy import Column, Integer, String, ForeignKey, Boolean
from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlalchemy.sql.expression import text
from .database import Base


# Database model
class GetPost(Base):
    __tablename__ = "posts"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    content = Column(String)
    published = Column(Boolean, default=True)
    created_at = Column(TIMESTAMP(timezone=True), 
                                  nullable=False, server_default=text('now()'))
    owner_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    
    

class User(Base):
    """Model representing a user."""
    __tablename__ = "users"

    id: int = Column(Integer, primary_key=True, nullable=False)
    username: str = Column(String, nullable=False, index=True)
    email: str = Column(String, unique=True, index=True, nullable=False)
    password: str = Column(String, nullable=False)
    is_active: bool = Column(Boolean, nullable=False, default=True)
    created_at = Column(TIMESTAMP(timezone=True), 
                                  nullable=False, server_default=text('now()'))
  

# class GetPost(Base):
#     __tablename__ = 'posts'

#     id = Column(Integer, primary_key=True, nullable=False)
#     title = Column(String, nullable=False)
#     content = Column(String, nullable=False)
#     published = Column(Boolean, server_default='TRUE', default=True, nullable=False)
#     created_at = Column(TIMESTAMP(timezone=True), 
#                                   nullable=False, server_default=text('now()'))




    # author_id = Column(Integer, ForeignKey('users.id'))
    # author = relationship('User', back_populates='posts')
    # comments = relationship('Comment', back_populates='post')
    # likes = relationship('Like', back_populates='post')
