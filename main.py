from gettext import find
import time
from fastapi import FastAPI, Body, Response, status, HTTPException
import psycopg2
from psycopg2.extras import RealDictCursor
from pydantic import BaseModel
from typing import Optional
from random import randrange

app = FastAPI()

# Pydantic Schema of POST
class Post(BaseModel):
    title : str
    content : str
    published : bool = True
    rating : Optional[float] = None
    id : Optional[int] = None


# Psycopg2 (Postgres) database connection
while True:
    
    try:
        conn = psycopg2.connect(host='localhost', database='fastapi-course', user='postgres', password='admin', cursor_factory=RealDictCursor)
        cursor = conn.cursor()
        print("Postgres Database connection was succesfull!")
        break
    except Exception as error:
        print("Connection to Postgres Database failed")
        print("Error:", error)
        time.sleep(3)
    
    
# temp data of POST
my_posts = [{"title": "hello world", "content": "this is my fastapi", "published": False, "rating": 4.1, "id": 1},
            {"title": "stuff", "content": "this is my stuff", "published": True, "rating": 4.9, "id": 2},
            {"title": "boring", "content": "this is my boring", "published": False, "rating": 3.8, "id": 3}]



# find post by id for temp data of POST
def find_post_by_id(id):
    for p in my_posts:
        if p['id'] == id:
            return p
        
        
# find post index by id for temp data of POST
def find_index_of_post(id):
    for i, p in enumerate(my_posts):
        if p['id'] == id:
            return i
        
        
# default endpoint
@app.get("/")
def root():
    return {"message" : "Hello World"}


# Post endpoint for creating new POST
@app.post("/new_posts", status_code=status.HTTP_201_CREATED)
def new_posts(post: Post):
    cursor.execute("""INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING * """, (post.title, post.content, post.published),)
    new_post = cursor.fetchone()
    conn.commit()
    
    # post_dict = post.model_dump() # use model_dump bcz dict is deprecated
    # post_dict['id'] = randrange(0, 100)
    # my_posts.append(post_dict)
    # print(post_dict) 
    
    return {"data" : f"created post {new_post}"}


# Get post by id
@app.get("/posts/{id}")
def get_post_by_id(id : int, response: Response):
    cursor.execute("""SELECT * FROM posts WHERE id = %s""",(id,))
    post = cursor.fetchone()
    
    # post = find_post_by_id(id)
    
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} was not found")
    print(post)
    return {"post_detail": post}


# Get all post
@app.get("/posts")
def get_posts():
    cursor.execute("""SELECT * FROM posts""")
    post = cursor.fetchall()
    return {"data": post}


# Delete post by id 
@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
    cursor.execute(""" DELETE FROM posts WHERE id = %s RETURNING * """, str(id),)
    post = cursor.fetchone()
    conn.commit()
    
    # index = find_index_of_post(id)
    
    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail = f"post with id: {id} was not found")
        
    # my_posts.pop(index)
    # return Response(status_code=status.HTTP_204_NO_CONTENT)
    
    return {"message" : f"post: {post} deleted"}
    
    
# Update post by id
@app.put("/posts/{id}", status_code=status.HTTP_200_OK)
def update_post(id: int, post: Post):
    cursor.execute("""UPDATE posts SET title = %s, content = %s, published = %s  WHERE id = %s RETURNING *""", (post.title, post.content, post.published, id,))
    updated_post = cursor.fetchone()
    conn.commit()
    
    # index = find_index_of_post(id)
    
    if updated_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail = f"post with id: {id} was not found")
    
    # post_dict = post.model_dump()
    # post_dict['id'] = id
    # my_posts[index] = post_dict
    
    return {"data": f"updated post {updated_post}"}
        
    


# @app.post("/createposts")
# def create_posts(payload: dict = Body(...)):
#     print(payload)
#     return {"new_post": f"title: {payload['title']}, content: {payload['content']}"}


