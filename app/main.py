from random import randrange
import time
from typing import Optional
from fastapi import FastAPI, Response, status, HTTPException, Depends
from fastapi.params import Body
from pydantic import BaseModel
import psycopg2
from psycopg2.extras import RealDictCursor
from sqlalchemy.orm import Session
from . import models
from .database import engine, get_db


models.Base.metadata.create_all(bind=engine)


app = FastAPI()


class Post(BaseModel):
    title: str
    content: str
    published: bool = False


while True:
    try:
        conn = psycopg2.connect(
            host="localhost",
            database="fastapi",
            user="postgres",
            password="shubham",
            cursor_factory=RealDictCursor,
        )
        cursor = conn.cursor()
        print("Connected to database")
        break
    except Exception as error:
        print("Connecting to database failed")
        print("Error", error)
        time.sleep(5)

my_posts = [
    {
        "title": "My first post",
        "content": "This is my first post",
        "published": True,
        "id": 1,
    },
    {
        "title": "My second post",
        "content": "This is my second post",
        "published": True,
        "id": 2,
    },
]


def find_post(post_id: int):
    for post in my_posts:
        if post["id"] == post_id:
            return post
    return None


def find_index_post(id: int):
    for i, post in enumerate(my_posts):
        if post["id"] == id:
            return i
    return None


@app.get("/posts")
def get_posts(db: Session = Depends(get_db)):
    posts = db.query(models.Post).all()
    return {"posts": posts}


@app.get("/sqlalchemy")
def test_post(db: Session = Depends(get_db)):
    posts = db.query(models.Post).all()
    for post in posts:
        print(post.title, post.content, post.published, post.created_at)
    return {"Status": posts}


@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_posts(post: Post):
    cursor.execute(
        """INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING * """,
        (post.title, post.content, post.published),
    )
    new_post = cursor.fetchone()
    conn.commit()
    return {"data": new_post}


@app.get("/posts/{id}")
def get_post(id: int, db: Session = Depends(get_db)):
    post = db.query(models.Post).filter(models.Post.id == id).first()
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Post not found"
        )
    return post


@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db)):
    post = db.query(models.Post).filter(models.Post.id == id)
    if not post.first():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Post not found"
        )
    post.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.put("/posts/{id}")
def update_post(id: int, post: Post, db: Session = Depends(get_db)):
    post = db.query(models.Post).filter(models.Post.id == id)
    if not post.first():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Post not found"
        )
    post.update(
        {"title": post.title, "content": post.content, "published": post.published}
    )
    db.commit()
    return {"data": "Post updated successfully"}
