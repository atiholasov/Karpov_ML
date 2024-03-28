from typing import List
from sqlalchemy.orm import Session
from sqlalchemy import func, desc
from database import SessionLocal
from models import MarkupStatusModel, CvatProjectModel, CvatProjectDumpModel
from schema import CvatProject, MarkupStatus, CvatProjectDump
from fastapi import FastAPI, Depends, HTTPException
from pydantic import BaseModel

app = FastAPI()


class RequestForm(BaseModel):
    project: str
    task_list: list


def get_db():
    with SessionLocal() as db:
        return db


@app.post("/db", response_model=List[CvatProject])
def get_users_feed(tasks_and_cvatPj: RequestForm, db: Session = Depends(get_db)):
    out = (db.query(CvatProjectModel)
           .all())
    print(out)
    return out