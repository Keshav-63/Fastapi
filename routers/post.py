from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from database import get_db
import models, schemas, oauth2

router = APIRouter(
    prefix="/posts",
    tags= ['Posts']
)


# Post endpoint for creating new POST
@router.post("/new_posts", status_code=status.HTTP_201_CREATED, response_model=schemas.PostOut)
def new_posts(post: schemas.PostCreate, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    
    new_post = models.Post(user_id=current_user.id, **post.dict()) # another way to list down fields is to use **post.dict() and unpack the dict eg. new_post = models.Post(**post.dict())
    print(new_post)
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
@router.get("/{id}", response_model=schemas.PostOut)
def get_post_by_id(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    # cursor.execute("""SELECT * FROM posts WHERE id = %s""",(id,))
    # post = cursor.fetchone()
    
    post = db.query(models.Post).filter(models.Post.id == id).first()
    
    # post = find_post_by_id(id)
    
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} was not found")
    
    if post.user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not Authorized")
    
    return post


# Get all post
@router.get("/", response_model=list[schemas.PostOut])
def get_posts(db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user), limit: int = 10, skip: int = 0, search: Optional[str] = ""):
    posts = db.query(models.Post).filter(models.Post.user_id == current_user.id).limit(limit).offset(skip).all()
    
    # cursor.execute("""SELECT * FROM posts""")
    # post = cursor.fetchall()
    return posts


# Delete post by id 
@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    # cursor.execute(""" DELETE FROM posts WHERE id = %s RETURNING * """, str(id,))
    # post = cursor.fetchone()
    # conn.commit()
    
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()
    
    # index = find_index_of_post(id)
    
    if post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail = f"post with id: {id} was not found")
    
    if post.user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not Authorized")
        
    post_query.delete(synchronize_session=False)
    db.commit()
    
    # my_posts.pop(index)
    # return Response(status_code=status.HTTP_204_NO_CONTENT)
    
    return
    
    
# Update post by id
@router.put("/{id}", status_code=status.HTTP_200_OK, response_model=schemas.PostOut)
def update_post(id: int, post: schemas.PostUpdate, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    # cursor.execute("""UPDATE posts SET title = %s, content = %s, published = %s  WHERE id = %s RETURNING *""", (post.title, post.content, post.published, id,))
    # updated_post = cursor.fetchone()
    # conn.commit()
    
    post_query = db.query(models.Post).filter(models.Post.id == id)
    updated_post = post_query.first() 
    
    # index = find_index_of_post(id)
    
    if updated_post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail = f"post with id: {id} was not found")
        
    if updated_post.user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not Authorized")
    
    post_query.update(post.dict(), synchronize_session=False)
    db.commit()
    
    # post_dict = post.model_dump()
    # post_dict['id'] = id
    # my_posts[index] = post_dict
    
    return updated_post


# @app.post("/createposts")
# def create_posts(payload: dict = Body(...)):
#     print(payload)
#     return {"new_post": f"title: {payload['title']}, content: {payload['content']}"}




