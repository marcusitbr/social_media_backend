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
from app.endpoints.models import GetPost, User
from app.endpoints.database import SessionLocal, connect_to_database
from app.endpoints.schemas import Post, PostCreate, UserCreate, UserOut, UserLogin
from .routers import post, user, auth


from fastapi.middleware.cors import CORSMiddleware

#from app.endpoints.database import connect_to_database




#create the database schema based on the models you have defined.
models.Base.metadata.create_all(bind=engine)
# Create tables in the database
User.metadata.create_all(bind=engine)

# Creates an instance of the FastAPI class, representing our web application.
app = FastAPI()

origins = ["https://www.google.com"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)


    


@app.get("/")
async def main():
    return {"message": "Hello World"}





