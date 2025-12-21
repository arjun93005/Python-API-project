from typing import Optional
from fastapi import FastAPI, Response, status, HTTPException
from fastapi import Body
from pydantic import BaseModel
import pydantic
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor
import time

app = FastAPI()

class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    rating: Optional[int] = None

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
                            

def find_post(id):
    f = 0
    for i in my_posts:
        if i['id'] == id:
            return i
    return None

def find_index_post(id):
    for i, p in enumerate(my_posts):
        if p['id'] == id:
            return i

@app.get("/")
def root():
    return {"hello world"}

@app.get("/posts")
def read_root():
    cursor.execute("SELECT * FROM posts")
    posts = cursor.fetchall()
    conn.commit()
    return {"data": posts}

@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_post(post: Post):
    cursor.execute("INSERT INTO posts (title, content) values (%s, %s) RETURNING *", (post.title, post.content))
    new_post = cursor.fetchone()
    conn.commit()
    return {"data": new_post}

@app.get("/posts/{id}")
def get_post(id: int, response: Response):
    if find_post(id) is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} was not found")
        # response.status_code = status.HTTP_404_NOT_FOUND
        # return {"message": f"post with id: {id} was not found"}

    return {"post": find_post(id)}

@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id : int):
    index  = my_posts.pop(find_index_post(id))
    if index is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} does not exist")
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@app.put("/posts/{id}")
def update_post(id: int, post: Post):
    index = find_index_post(id)
    if index is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} does not exist")
    
    post_dict = post.dict()
    post_dict['id'] = id
    my_posts[index] = post_dict
    return {"data": my_posts[index]}