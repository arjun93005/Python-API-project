from typing import Optional, List
from fastapi import FastAPI, Response, status, HTTPException, Depends
from pydantic import BaseModel
import pydantic
# from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from . import models
from .database import engine, get_db
from sqlalchemy.orm import Session
from .routers import post, user, auth

models.base.metadata.create_all(bind=engine)

app = FastAPI()

while True:
    try:
        conn = psycopg2.connect(host='localhost', database='fastapi', user='postgres', password = '123arjun123', cursor_factory=RealDictCursor)
        cursor = conn.cursor()
        print("Database connection was successful")
        break
    except Exception as e:
        print("Unable to connect to the database")
        print("Error:", e)
        time.sleep(2)
                            

# def find_post(id):
#     f = 0
#     for i in my_posts:
#         if i['id'] == id:
#             return i
#     return None

# def find_index_post(id):
#     for i, p in enumerate(my_posts):
#         if p['id'] == id:
#             return i

# @app.get("/")
# def root():
#     return {"hello world"}

app.include_router(auth.router)
app.include_router(user.router)
app.include_router(post.router)

#https://www.youtube.com/watch?v=ToXOb-lpipM&list=PL8VzFQ8k4U1IiGUWdBI7s9Y7dm-4tgCXJ&index=2
# uvicorn app.main:app --reload
# 7:34:54