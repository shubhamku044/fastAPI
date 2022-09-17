from typing import Optional
from fastapi import FastAPI
from fastapi.params import Body
from pydantic import BaseModel

app = FastAPI()


class Post(BaseModel):
    fName: str
    lName: str
    age: int
    publish: bool = False
    rating: Optional[int] = None


@app.get("/")
def read_root():
    return {"message": "Welcome to my api"}


@app.post("/")
def post_root(newPost: Post):

    # We need fName and lName

    data = {
        "first name": newPost.fName,
        "last name": newPost.lName,
        "age": newPost.age,
        "publish": newPost.publish,
        "rating": newPost.rating,
    }
    # print(newPost.dict())
    return {"data": newPost.dict()}
