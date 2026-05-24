from fastapi import FastAPI, Body
from pydantic import BaseModel
from typing import Optional
from random import randrange

app = FastAPI()

class Post(BaseModel):
    title : str
    content : str
    published : bool = True
    rating : Optional[float] = None
    id : Optional[int] = None


my_posts = [{"title": "hello world", "content": "this is my fastapi", "published": False, "rating": 4.1, "id": 1},
            {"title": "stuff", "content": "this is my stuff", "published": True, "rating": 4.9, "id": 2},
            {"title": "boring", "content": "this is my boring", "published": False, "rating": 3.8, "id": 3}]


def find_post_by_id(id):
    for p in my_posts:
        if p['id'] == id:
            return p

@app.get("/")
def root():
    return {"message" : "Hello World"}


@app.post("/new_posts")
def new_posts(new_post: Post):
    post_dict = new_post.model_dump() # use model_dump bcz dict is deprecated
    post_dict['id'] = randrange(0, 100)
    my_posts.append(post_dict)
    print(post_dict) 
    return {"data" : post_dict}


@app.get("/posts/{id}")
def get_post_by_id(id : int):
    post = find_post_by_id(id)
    print(post)
    return {"post_detail": post}


@app.get("/posts")
def get_posts():
    return {"data": my_posts}
    

@app.post("/createposts")
def create_posts(payload: dict = Body(...)):
    print(payload)
    return {"new_post": f"title: {payload['title']}, content: {payload['content']}"}
