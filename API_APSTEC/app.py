from sqlalchemy.orm import Session
from sqlalchemy import func, desc, insert, update
from database import SessionLocal
from models import MarkupStatusModel, CvatProjectModel, CvatProjectDumpModel, DumpModel
from schema import CvatProject, MarkupStatus, CvatProjectDump
from fastapi import FastAPI, Depends, HTTPException
from pydantic import BaseModel
import logging

app = FastAPI()
logging.basicConfig(level=logging.INFO, filename="app_log.log", filemode="a",
                    format="%(asctime)s %(levelname)s %(message)s")


class RequestForm(BaseModel):
    project: str
    status: str
    task_list: list


def get_db():
    with SessionLocal() as db:
        return db


@app.post("/add/project_status")
def send_info_after_cvat_creating(tasks_and_cvat_project: RequestForm, db: Session = Depends(get_db)):
    """
    Puts up cvat_project_name and status of tasks into database after cvat_creating pipline
    :param tasks_and_cvat_project: Json with posted data
    :param db: Session example
    :return: Status of request
    """

    def get_dump_id(task_list_: list):
        dumps_id_ = db.query(DumpModel.id).where(DumpModel.name.in_(tuple(task_list_))).all()
        logging.info(f"Successfully received dumps_id: {dumps_id_} for task_list: {task_list_} from DB.")
        return dumps_id_

    def get_project_id(project_name_: str):
        cvat_project_id = db.query(CvatProjectModel.id).where(CvatProjectModel.name == f'{project_name_}').one_or_none()
        logging.info(
            f"Successfully received cvat_project_id: {cvat_project_id} for project_name: {project_name_} from DB.")
        return cvat_project_id

    def add_project_name(project_name_: str):
        new_project = CvatProjectModel(name=project_name_)
        db.add(new_project)
        db.commit()
        cvat_project_id = get_project_id(project_name_)
        logging.info(
            f"Successfully added cvat_project_id: {cvat_project_id} for project_name: {project_name_} into DB.")
        return cvat_project_id

    def get_status_id(status_: str):
        status_id_ = db.query(MarkupStatusModel.id).where(MarkupStatusModel.name == f'{status_}').one_or_none()
        logging.info(f"Successfully received status_id: {status_id_} for status: {status_} from DB.")
        return status_id_

    def add_cvat_project_dump(project_id_, status_id_, dumps_id_):
        pillar_indexes = (1, 2)
        for dump in dumps_id_:
            for pillar_index in pillar_indexes:
                new_record = CvatProjectDumpModel(
                    dump_id=dump[0],
                    cvat_project_id=project_id_[0],
                    status_id=status_id_[0],
                    pillar_num=pillar_index)
                db.add(new_record)
                db.commit()
        logging.info(
            f"Successfully added project_id: {project_id_} for dumps_id: {dumps_id_} into DB with status_id: {status_id_}.")

    def get_cvat_dump_id(dumps_id_):
        list_dumps_id_ = [el[0] for el in dumps_id_]
        cvat_dump_id_ = db.query(CvatProjectDumpModel.id).where(
            CvatProjectDumpModel.dump_id.in_(tuple(list_dumps_id_))).all()
        logging.info(f"Successfully received cvat_dump_id: {cvat_dump_id_} for dumps_id: {dumps_id_} from DB.")
        return cvat_dump_id_

    def change_cvat_dump_name_and_status(project_id_, status_id_, cvat_dump_id_):
        list_cvat_dump_id_ = [el[0] for el in cvat_dump_id_]
        stmt = (
            update(CvatProjectDumpModel)
            .values(status_id=status_id_[0], cvat_project_id=project_id_[0])
            .where(CvatProjectDumpModel.id.in_(tuple(list_cvat_dump_id_)))
        )
        db.execute(stmt)
        db.commit()
        logging.info(
            f"Successfully changed project_id: {project_id_} and status_id: {status_id_} for cvat_dump_id: {cvat_dump_id_} in DB.")

    # MAIN CYCLE

    logging.info("NEW CALL send_info_after_cvat_creating()")
    logging.info("Into API was send the json with next filling:")
    logging.info(f"Json: {tasks_and_cvat_project}")

    try:
        dumps_id = get_dump_id(tasks_and_cvat_project.task_list)
    except Exception as err:
        logging.error(f"Problems with call get_dump_id(), {err}")
        return "Problems with call get_dump_id()"
    try:
        project_name = tasks_and_cvat_project.project
    except Exception as err:
        logging.error(f"Problems with get project_name from json, {err}")
        return "Problems with get project_name from json"
    try:
        status = tasks_and_cvat_project.status
    except Exception as err:
        logging.error(f"Problems with get status from json, {err}")
        return "Problems with get status from json"

    if not dumps_id:
        logging.info("Unsuccessful. There was no change into database, because dumps from config are not into DataBase")
        return "Unsuccessful. There was no change into database, because dumps from config are not into DataBase"
    if len(dumps_id) != len(tasks_and_cvat_project.task_list):
        logging.info("Unsuccessful. There was no change into database, because dumps from config are into DataBase only"
                     "partial")
        return ("Unsuccessful. There was no change into database, because dumps from config are into DataBase only"
                "partial")

    try:
        project_id = get_project_id(project_name)
        if project_id is None:
            project_id = add_project_name(project_name)
    except Exception as err:
        logging.error(f"Problems with get_project_id() or add_project_name(), {err}")
        return "Problems with get_project_id() or add_project_name()"

    try:
        status_id = get_status_id(status)
    except Exception as err:
        logging.error(f"Problems with get_status_id(), {err}")
        return "Problems with get_status_id()"

    try:
        cvat_dump_id = get_cvat_dump_id(dumps_id)
    except Exception as err:
        logging.error(f"Problems with get_cvat_dump_id(), {err}")
        return "Problems with get_cvat_dump_id()"

    if not cvat_dump_id:
        try:
            add_cvat_project_dump(project_id, status_id, dumps_id)
        except Exception as err:
            logging.error(f"Problems with add_cvat_project_dump(), {err}")
            return "Problems with add_cvat_project_dump()"

    elif len(cvat_dump_id) != 2 * len(tasks_and_cvat_project.task_list):
        try:
            change_cvat_dump_name_and_status(project_id, status_id, cvat_dump_id)
        except Exception as err:
            logging.error(f"Problems with change_cvat_dump_name_and_status(), {err}")
            return "Problems with change_cvat_dump_name_and_status()"

    else:
        logging.info("Unsuccessful. There was no change into database, because same cvat_project_dumps already in "
                     "DataBase, but not all")
        return ("Unsuccessful. There was no change into database, because same cvat_project_dumps already in DataBase, "
                "but not all")
