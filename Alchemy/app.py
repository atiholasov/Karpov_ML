from typing import List

from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

from database import SessionLocal
from table_feed import Post, User, Feed
from schema import PostGet, UserGet, FeedGet

app = FastAPI()


def get_db():
    with SessionLocal() as db:
        return db


@app.get("/user/{id}", response_model=UserGet)
def get_all_users(id: int, db: Session = Depends(get_db)):
    result = db.query(User).filter(User.id == id).one_or_none()
    if result == None:
        raise HTTPException(status_code=404, detail="user not found")
    return result


@app.get("/post/{id}", response_model=PostGet)
def get_all_post(id: int, db: Session = Depends(get_db)):
    result = db.query(Post).filter(Post.id == id).one_or_none()
    if result == None:
        raise HTTPException(status_code=404, detail="post not found")
    return result


@app.get("/user/{id}/feed", response_model=List[FeedGet])
def get_users_feed(id: int, limit=10, db: Session = Depends(get_db)):
    result = db.query(Feed).filter(Feed.user_id == id).order_by(Feed.time.desc()).limit(limit).all()
    return result


@app.get("/post/{id}/feed", response_model=List[FeedGet])
def get_post_feed(id: int, limit=10, db: Session = Depends(get_db)):
    result = db.query(Feed).filter(Feed.post_id == id).order_by(Feed.time.desc()).limit(limit).all()
    return result