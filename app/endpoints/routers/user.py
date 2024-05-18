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
from app.endpoints import models, utils
# from ..models.post import Post
from app.endpoints.models import User
from app.endpoints.database import SessionLocal, connect_to_database
from app.endpoints.schemas import Post, UserCreate, UserOut, UserUpdate

router = APIRouter(
    prefix="/users",
    tags=["Users"]
)



class UserController:

    @router.post("/", status_code=status.HTTP_201_CREATED, response_model=UserCreate)
    async def create_user(user: UserCreate):

        hashed_password = utils.hash(user.password)
        user.password = hashed_password

        try:
            conn, cursor = connect_to_database()
            try:
                cursor.execute("""
                    INSERT INTO users (username, email, password, is_active)
                    VALUES (%s, %s, %s, %s)
                    RETURNING *
                """, (user.username, user.email, user.password, user.is_active))

                new_user = cursor.fetchone()
                conn.commit()
                return UserCreate(**new_user)
            finally:
                cursor.close()
                conn.close()
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
        
    @router.get("/{user_id}")
    def get_user_by_id(user_id: int, db: Session = Depends(get_db)):
        try:
            user = db.query(models.User).filter(models.User.id == user_id).first()
            db.close()
            if user is None:
                raise HTTPException(status_code=404, detail="User not found")
            return user
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
    
        from fastapi import HTTPException

    @router.get("/")
    def get_all_users(db: Session = Depends(get_db)):
        try:
            users = db.query(models.User).all()
            db.close()
            return users
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    @router.put("/{user_id}")
    def update_user(user_id: int, user_update: UserUpdate, db: Session = Depends(get_db)):
        try:
            user = db.query(models.User).filter(models.User.id == user_id).first()
            if user is None:
                raise HTTPException(status_code=404, detail="User not found")

            # Update user fields
            for field, value in user_update.dict().items():
                setattr(user, field, value)

            db.commit()
            return {"message": "User updated successfully"}

        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

        
    
@router.delete("/{user_id}")
async def delete_user(user_id: int):
    conn, cursor = connect_to_database()
    cursor.execute("""DELETE FROM users WHERE id = %s RETURNING * """, (user_id,))
    deleted_user = cursor.fetchone()
    conn.commit()
    
    if not deleted_user:
        raise HTTPException(status_code=404, detail=f"User with id {user_id} was not found")

    return {"message": "User deleted successfully"}