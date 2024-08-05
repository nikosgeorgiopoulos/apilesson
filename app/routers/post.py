from curses.ascii import HT
from fastapi import FastAPI ,  Response ,  status , HTTPException, Depends , APIRouter
from .. import models , schemas , utils , oauth2 
from ..database import get_db
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import Optional , List

import app



router = APIRouter(
    prefix="/posts",
    tags= ['posts']
)

#, response_model = List[schemas.PostResponse]
#, response_model = List[schemas.PostVoteResponse]
@router.get("/", response_model = List[schemas.PostVote] )
def get_posts(db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user), 
              limit: int = 10 , skip: int = 0 , search: Optional[str] = ""):
    
    
    
    # posts = db.query(models.Post).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()  
    

    posts = db.query(models.Post , func.count(models.Vote.post_id).label("votes")).join(
        models.Vote, models.Vote.post_id == models.Post.id , isouter=True).group_by(models.Post.id).filter(
            models.Post.title.contains(search)).limit(limit).offset(skip).all()


    return  posts          




@router.get("/{id}", status_code=status.HTTP_302_FOUND, response_model = schemas.PostVote)
def get_one_post(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
   
    

    # post = db.query(models.Post).filter(models.Post.id == id).first()

    post = db.query(models.Post , func.count(models.Vote.post_id).label("votes")).join(
        models.Vote, models.Vote.post_id == models.Post.id , isouter=True).group_by(models.Post.id).filter(models.Post.id == id).first()
    
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f"post with id: {id} was not found")
    
    
    return post





@router.post("/", status_code=status.HTTP_201_CREATED, response_model = schemas.PostResponse)
def create(post: schemas.PostCreate , db: Session = Depends(get_db), current_user: str = Depends(oauth2.get_current_user)):
   

    #print(current_user.email)

    new_post = models.Post(creator_id = current_user.id , **post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)


    return new_post




@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):

    post_delete_query = db.query(models.Post).filter(models.Post.id == id)

    post = post_delete_query.first()

    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id:{id} does not exist")
    

    if post.creator_id != current_user.id:
        raise HTTPException(status.HTTP_403_FORBIDDEN , detail = "Unauthorized to perform this action.")

    post_delete_query.delete(synchronize_session= False)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)



@router.put("/{id}", response_model = schemas.PostResponse)
def update_post(id: int, updated_post: schemas.PostCreate, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):

    
    post_put_query = db.query(models.Post).filter(models.Post.id == id)
    
    post = post_put_query.first() 
    
    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id:{id} does not exist")
    
    if post.creator_id != current_user.id:
        raise HTTPException(status.HTTP_403_FORBIDDEN , detail = "Unauthorized to perform this action.")


    post_put_query.update( updated_post.dict() ,  synchronize_session=False)
    
    db.commit()
    
    return post_put_query.first()