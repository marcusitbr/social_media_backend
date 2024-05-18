# Imports the FastAPI class from the fastapi module.
from fastapi import FastAPI, Response
from fastapi.params import Body
from pydantic import BaseModel, Field
from typing import Optional, List
from random import randrange

from fastapi import FastAPI, HTTPException, Depends, status, APIRouter
from datetime import datetime
#from app.routes.retrieve_post import Post
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from sqlalchemy.orm import Session
#from app.models import Post
from app.endpoints.database import engine, get_db
from app.endpoints import models, utils, oauth2
# from ..models.post import Post
from app.endpoints.models import GetPost, User
from app.endpoints.database import SessionLocal, connect_to_database
from app.endpoints.schemas import Post, PostCreate, UserOut

router = APIRouter(
    prefix="/posts",
    tags=["Posts"]
)

# class PostController:
#     @router.post("/", status_code=status.HTTP_201_CREATED, response_model=Post)
#     def create_post(post: PostCreate, current_user: models.User = Depends(oauth2.get_current_user), db: Session = Depends(get_db)):
#         try:
#             # Create a new post instance with owner_id set to the current user's ID
#             new_post = models.Post(title=post.title, content=post.content, published=post.published, owner_id=current_user.id, created_at=datetime.now())
            
#             # Add the new post to the database session
#             db.add(new_post)
#             # Commit the transaction
#             db.commit()
#             # Refresh the instance to fetch the auto-generated ID
#             db.refresh(new_post)
            
#             # Return the newly created post
#             return new_post
#         except Exception as e:
#             # Rollback the transaction in case of error
#             db.rollback()
#             raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


class PostController:
    @router.post("/", status_code=status.HTTP_201_CREATED, response_model=Post)
    def create_post(post: PostCreate, current_user: User = Depends(oauth2.get_current_user), db: Session = Depends(get_db)):
        try:
            # Establish a connection to the database
            conn, cursor = connect_to_database()
            try:
                # Execute the SQL query to insert a new post
                cursor.execute(
                    """INSERT INTO posts (title, content, published, owner_id) VALUES (%s,%s, %s, %s) RETURNING *""",
                    (post.title, post.content, post.published, post.owner_id)
                )
                # Fetch the newly created post from the database
                new_post = cursor.fetchone()
                # Commit the transaction
                conn.commit()
                # Close cursor and connection
                cursor.close()
                conn.close()
                # Return the newly created post
                return new_post
            except Exception as e:
                # Rollback the transaction in case of error
                conn.rollback()
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
        except Exception as e:
            # Raise HTTPException for database connection error
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))




      
# We define a single endpoint /posts/{post_id} to retrieve a post by its ID.
        
class PostService:
    @router.get("/")
    def get_posts(db: Session = Depends(get_db)):
        try:
            # db = SessionLocal()
            posts = db.query(models.GetPost).all()
            db.close()
            return posts
            # return {"social_post_data": [post.__dict__ for post in posts]}
        except Exception as e:
                raise HTTPException(status_code=500, detail=str(e))
    
    @router.get("/{post_id}")
    def get_post_by_id(post_id: int, db: Session = Depends(get_db)):
        try:
            post = db.query(models.GetPost).filter(models.GetPost.id == post_id).first()
            db.close()
            if post is None:
                raise HTTPException(status_code=404, detail="Post not found")
            return post
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

        
@router.delete("/{post_id}")
async def delete_post(post_id: int):
    conn, cursor = connect_to_database()
    cursor.execute("""DELETE FROM posts WHERE id = %s RETURNING * """, (post_id,))
    deleted_post = cursor.fetchone()
    conn.commit()
    
    if not deleted_post:
        raise HTTPException(status_code=404, detail=f"Post with id {post_id} was not found")

    return {"message": "Post deleted successfully"}


# Update a post by its ID
@router.put("/{id}")
async def update_post(id: int, post: PostCreate):
    conn, cursor = connect_to_database()
    cursor.execute("""
        UPDATE posts 
        SET title = %s, content = %s, published = %s 
        WHERE id = %s
        RETURNING * 
    """, (post.title, post.content, post.published, id))
    
    updated_post = cursor.fetchone()
    conn.commit()

    if updated_post is None:
        raise HTTPException(status_code=404, detail=f"Post with id: {id} not found")

    return {"message": "Post updated successfully"}

