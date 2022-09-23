from random import randrange
from typing import Optional
from fastapi import FastAPI, Response, status, HTTPException
from fastapi.params import Body
from pydantic import BaseModel

app = FastAPI()


class Post(BaseModel):
    title: str
    content: str
    published: bool = False
    rating: Optional[int] = None


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
def get_posts():
    return {"posts": my_posts}


@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_posts(post: Post):
    post_dict = post.dict()
    post_dict["id"] = randrange(1, 1000000)
    my_posts.append(post_dict)
    return {"post": post_dict}


@app.get("/posts/{id}")
def get_post(id: int):
    post = find_post(id)
    if not post:
        # response.status_code = status.HTTP_404_NOT_FOUND
        # return {"message": f"post with id: {id} not found"}
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"post with id: {id} not found",
        )
    return {"post": post}


@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
    index = find_index_post(id)

    if index == None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"post with id: {id} not found",
        )

    my_posts.pop(index)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
