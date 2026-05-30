import time
from fastapi import Depends, FastAPI, Response, status, HTTPException
import psycopg2
from psycopg2.extras import RealDictCursor
import models, schemas, utlis
from sqlalchemy.orm import Session
from database import engine, get_db
from routers import post, user

models.Base.metadata.create_all(bind=engine)

app = FastAPI()    

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
        
        
app.include_router(post.router)
app.include_router(user.router)
        
        
# default endpoint
@app.get("/")
def root():
    return {"message" : "Hello World"}


# sqlalchemy check
@app.get("/sqlalchemy")
def test_sqlalchemy(db: Session = Depends(get_db)):
    posts = db.query(models.Post).all()
    return {"data": posts}