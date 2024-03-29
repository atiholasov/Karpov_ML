from typing import List
from sqlalchemy.orm import Session
from sqlalchemy import func, desc, insert
from database import SessionLocal
from models import MarkupStatusModel, CvatProjectModel, CvatProjectDumpModel, DumpModel
from schema import CvatProject, MarkupStatus, CvatProjectDump
from fastapi import FastAPI, Depends, HTTPException
from pydantic import BaseModel

app = FastAPI()


class RequestForm(BaseModel):
    project: str
    status: str
    task_list: list


def get_db():
    with SessionLocal() as db:
        return db


@app.post("/show/cvatProjectDump", response_model=List[CvatProjectDump])
def get_users_feed(tasks_and_cvatPj: RequestForm, db: Session = Depends(get_db)):
    out = (db.query(CvatProjectModel)
           .where(CvatProjectDumpModel.cvat_project.name == f'{tasks_and_cvatPj.project}')
           .all())
    return out


@app.post("/add/project_status")
def send_info_after_cvat_creating(tasks_and_cvat_project: RequestForm, db: Session = Depends(get_db)):
    """
    Bla bla bla
    :param tasks_and_cvat_project:
    :param db:
    :return:
    """

    def get_dump_id(task_list_: list):
        dumps_id_ = db.query(DumpModel.id).where(DumpModel.name.in_(tuple(task_list_))).all()
        return dumps_id_

    def get_project_id(project_name_: str):
        cvat_project_id = db.query(CvatProjectModel.id).where(CvatProjectModel.name == f'{project_name_}').one_or_none()
        return cvat_project_id

    def add_project_name(project_name_: str):
        new_project = CvatProjectModel(name=project_name_)
        db.add(new_project)
        db.commit()
        cvat_project_id = get_project_id(project_name_)
        return cvat_project_id

    def get_status_id(status_: str):
        status_id_ = db.query(MarkupStatusModel.id).where(MarkupStatusModel.name == f'{status_}').one_or_none()
        return status_id_

    def add_cvat_project_dump():
        new_pj = CvatProjectDumpModel(
            dump_id=DumpModel(name='240212-142558'),
            cvat_project_id=CvatProjectModel(name='PJ_from_alchemy_2'),
            status_id=MarkupStatusModel(name='unmarked'),
            pillar_num=1)

        db.add(new_pj)
        db.commit()

    # MAIN CIRCLE

    dumps_id = get_dump_id(tasks_and_cvat_project.task_list)
    project_name = tasks_and_cvat_project.project
    status = tasks_and_cvat_project.status

    if not dumps_id:
        return "Unsuccessful. There was no change into database, because dumps from config are not into DataBase"

    project_id = get_project_id(project_name)
    if project_id is None:
        project_id = add_project_name(project_name)

    status_id = get_status_id(status)

    print(project_id)
    print(status_id)
    print(dumps_id)
    # add_cvat_project_dump()    ДОБАВИТЬ ЭТУ ФУНКЦИЮ
