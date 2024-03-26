from typing import List
from sqlalchemy.orm import Session
from sqlalchemy import func, desc
from database import SessionLocal
from table_feed import Post, User, Feed
from schema import PostGet, UserGet, FeedGet
from fastapi import FastAPI, Depends, HTTPException
from pydantic import BaseModel

app = FastAPI()


def get_db():
    with SessionLocal() as db:
        return db


class RequestForm(BaseModel):
    project: str
    task_list: list


app = FastAPI()


@app.post("/db", response_model=List[PostGet])
def get_users_feed(tasks_and_cvatPj: RequestForm, db: Session = Depends(get_db)):
    out = (db.query(Post)
           .select_from(Feed)
           .filter(Feed.action == 'like')
           .join(Post)
           .group_by(Post.id)
           .order_by(desc(func.count(Post.id)))
           .all())
    return out
