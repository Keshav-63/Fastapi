import time
from fastapi import Depends, FastAPI, Response, status, HTTPException
import psycopg2
from psycopg2.extras import RealDictCursor
import models, schemas, utlis
from sqlalchemy.orm import Session
from database import engine, get_db

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
        
        
# default endpoint
@app.get("/")
def root():
    return {"message" : "Hello World"}


# Post endpoint for creating new POST
@app.post("/new_posts", status_code=status.HTTP_201_CREATED, response_model=schemas.PostOut)
def new_posts(post: schemas.PostCreate, db: Session = Depends(get_db)):
    new_post = models.Post(**post.dict()) # another way to list down fields is to use **post.dict() and unpack the dict eg. new_post = models.Post(**post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    
           
    # Traditional way of inserting data into database using psycopg2 
    # cursor.execute("""INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING * """, (post.title, post.content, post.published,))
    # new_post = cursor.fetchone()
    # conn.commit()
    
    
    # post_dict = post.model_dump() # use model_dump bcz dict is deprecated
    # post_dict['id'] = randrange(0, 100)
    # my_posts.append(post_dict)
    # print(post_dict) 
    
    return new_post


# Get post by id
@app.get("/posts/{id}", response_model=schemas.PostOut)
def get_post_by_id(id : int, response: Response, db: Session = Depends(get_db)):
    # cursor.execute("""SELECT * FROM posts WHERE id = %s""",(id,))
    # post = cursor.fetchone()
    
    post = db.query(models.Post).filter(models.Post.id == id).first()
    
    # post = find_post_by_id(id)
    
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} was not found")
    return post


# Get all post
@app.get("/posts", response_model=list[schemas.PostOut])
def get_posts(db: Session = Depends(get_db)):
    posts = db.query(models.Post).all()
    
    # cursor.execute("""SELECT * FROM posts""")
    # post = cursor.fetchall()
    return posts


# Delete post by id 
@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db)):
    # cursor.execute(""" DELETE FROM posts WHERE id = %s RETURNING * """, str(id,))
    # post = cursor.fetchone()
    # conn.commit()
    
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()
    
    # index = find_index_of_post(id)
    
    if post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail = f"post with id: {id} was not found")
        
    post_query.delete(synchronize_session=False)
    db.commit()
    
    # my_posts.pop(index)
    # return Response(status_code=status.HTTP_204_NO_CONTENT)
    
    return
    
    
# Update post by id
@app.put("/posts/{id}", status_code=status.HTTP_200_OK, response_model=schemas.PostOut)
def update_post(id: int, post: schemas.PostUpdate, db: Session = Depends(get_db)):
    # cursor.execute("""UPDATE posts SET title = %s, content = %s, published = %s  WHERE id = %s RETURNING *""", (post.title, post.content, post.published, id,))
    # updated_post = cursor.fetchone()
    # conn.commit()
    
    post_query = db.query(models.Post).filter(models.Post.id == id)
    updated_post = post_query.first() 
    
    # index = find_index_of_post(id)
    
    if updated_post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail = f"post with id: {id} was not found")
    
    post_query.update(post.dict(), synchronize_session=False)
    db.commit()
    
    # post_dict = post.model_dump()
    # post_dict['id'] = id
    # my_posts[index] = post_dict
    
    return updated_post


# sqlalchemy check
@app.get("/sqlalchemy")
def test_sqlalchemy(db: Session = Depends(get_db)):
    posts = db.query(models.Post).all()
    return {"data": posts}


# @app.post("/createposts")
# def create_posts(payload: dict = Body(...)):
#     print(payload)
#     return {"new_post": f"title: {payload['title']}, content: {payload['content']}"}





# Users

@app.post("/users", status_code = status.HTTP_201_CREATED, response_model=schemas.UserOut)
def creat_users(create_user: schemas.UserCreate, db: Session = Depends(get_db)):
    user = models.User(**create_user.dict())
    user.password = utlis.hash(create_user.password)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user
