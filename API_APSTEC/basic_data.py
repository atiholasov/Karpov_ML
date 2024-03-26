from sqlalchemy import select, create_engine
from sqlalchemy.orm import Session, joinedload

from .models.models import Models


class BasicDataAlchemy:
    def __init__(self, DBUSER, DBPASSWORD, DBHOST, DBPORT, DBNAME) -> None:
        self.main_engine = create_engine(
            f'postgresql://{DBUSER}:{DBPASSWORD}@{DBHOST}:{DBPORT}/{DBNAME}',
            echo=False,
        )

    def get_data(self):
        with Session(bind=self.main_engine) as db:
            # start= datetime.datetime.now()
            simulant_query = select(Models.SimulantDumpModel.value).options(
                joinedload(Models.SimulantDumpModel.value.dump).options(
                    joinedload(Models.DumpModel.value.system),
                    joinedload(Models.DumpModel.value.geolocation),
                    joinedload(Models.DumpModel.value.ml_purpose),
                ),
                joinedload(Models.SimulantDumpModel.value.locationhrz),
                joinedload(Models.SimulantDumpModel.value.locationvrt),
                joinedload(Models.SimulantDumpModel.value.object),
                joinedload(Models.SimulantDumpModel.value.vector),
                joinedload(Models.SimulantDumpModel.value.orientation)
            )
            simulant_data = db.execute(simulant_query).all()
            cvat_dumps_query = select(Models.CvatProjectDumpModel.value).options(
                joinedload(Models.CvatProjectDumpModel.value.dump),
                joinedload(Models.CvatProjectDumpModel.value.status),
                joinedload(Models.CvatProjectDumpModel.value.cvat_project),
            )
            cvat_dumps_data = db.execute(cvat_dumps_query).all()
            data_dict = self.data_to_dict(simulant_data, cvat_dumps_data)
            return data_dict

    def commit_data_to_db(self, data: list):

        with Session(bind=self.main_engine) as db:

            for item in data:
                # data_changes = []
                # list_changes = []
                # list_of_old_prop = []

                if 'cvat_project' not in item:
                    print(item['name'], 'was skiped')
                    continue

                dump_query = db.execute(select(Models.DumpModel.value)
                                        .where(Models.DumpModel.value.name == item['name'])).scalar_one_or_none()

                if not dump_query:
                    raise Exception(item['name'])

                else:
                    cvat_project_from_datatable = db.execute(select(Models.CvatProjectModel.value)
                                                             .where(
                        Models.CvatProjectModel.value.name == item['cvat_project'])).scalar_one_or_none()

                    markup_status_from_datatable_pillar1 = db.execute(select(Models.MarkupStatusModel.value)
                                                                      .where(
                        Models.MarkupStatusModel.value.name == item['pillar1'])).scalar_one_or_none()

                    # if not markup_status_from_datatable_pillar1:
                    #     markup_status_from_datatable_pillar1 = Models.MarkupStatusModel.value(
                    #         name = item['pillar1']
                    #     )
                    #     db.add(markup_status_from_datatable_pillar1)
                    #     db.commit()

                    markup_status_from_datatable_pillar2 = db.execute(select(Models.MarkupStatusModel.value)
                                                                      .where(
                        Models.MarkupStatusModel.value.name == item['pillar2'])).scalar_one_or_none()

                    # if not markup_status_from_datatable_pillar2:
                    #     markup_status_from_datatable_pillar2 = Models.MarkupStatusModel.value(
                    #         name = item['pillar2']
                    #     )
                    #     db.add(markup_status_from_datatable_pillar2)
                    #     db.commit()

                    if not cvat_project_from_datatable:
                        cvat_project_from_datatable = Models.CvatProjectModel.value(
                            name=item['cvat_project']
                        )
                        db.add(markup_status_from_datatable_pillar2)
                        db.commit()

                    cvat_project_dump_pillar1 = db.execute(select(Models.CvatProjectDumpModel.value)
                                                           .where(
                        (Models.CvatProjectDumpModel.value.dump_id == dump_query.id) &
                        (Models.CvatProjectDumpModel.value.pillar_num == 1))).scalar_one_or_none()
                    if cvat_project_dump_pillar1:
                        # for cvat_project_dump in cvat_project_dumps:
                        if cvat_project_dump_pillar1.cvat_project.name != cvat_project_from_datatable.name:
                            # list_of_old_prop.append(f'OLD cvat_project pillar 1: {cvat_project_dump_pillar1.cvat_project.name}')
                            cvat_project_dump_pillar1.cvat_project.name = cvat_project_from_datatable.name
                            # list_changes.append(f'NEW cvat_project pillar 1: {cvat_project_dump_pillar1.cvat_project.name}')

                        if cvat_project_dump_pillar1.status_id != markup_status_from_datatable_pillar1.id:
                            # list_of_old_prop.append(f'OLD status pillar 1: {cvat_project_dump_pillar1.status.name}')
                            cvat_project_dump_pillar1.status = markup_status_from_datatable_pillar1
                            # list_changes.append(f'NEW status pillar 1 : {cvat_project_dump_pillar1.status.name}')
                        db.commit()
                    else:
                        cvat_project_dump1 = Models.CvatProjectDumpModel.value(
                            dump=dump_query,
                            cvat_project=cvat_project_from_datatable,
                            pillar_num=1,
                            status=markup_status_from_datatable_pillar1
                        )
                        db.add(cvat_project_dump1)
                        db.commit()

                    cvat_project_dump_pillar2 = db.execute(select(Models.CvatProjectDumpModel.value)
                                                           .where(
                        (Models.CvatProjectDumpModel.value.dump_id == dump_query.id) &
                        (Models.CvatProjectDumpModel.value.pillar_num == 2))).scalar_one_or_none()
                    if cvat_project_dump_pillar2:
                        # for cvat_project_dump in cvat_project_dumps:
                        if cvat_project_dump_pillar2.cvat_project.name != cvat_project_from_datatable.name:
                            # list_of_old_prop.append(f'OLD cvat_project pillar 2: {cvat_project_dump_pillar2.cvat_project.name}')
                            cvat_project_dump_pillar2.cvat_project.name = cvat_project_from_datatable.name
                            # list_changes.append(f'NEW cvat_project pillar 2: {cvat_project_dump_pillar2.cvat_project.name}')

                        if cvat_project_dump_pillar2.status_id != markup_status_from_datatable_pillar2.id:
                            # list_of_old_prop.append(f'OLD status pillar 2: {cvat_project_dump_pillar2.status.name}')
                            cvat_project_dump_pillar2.status = markup_status_from_datatable_pillar2
                            # list_changes.append(f'NEW status pillar 2: {cvat_project_dump_pillar2.status.name}')
                        db.commit()
                    else:
                        cvat_project_dump2 = Models.CvatProjectDumpModel.value(
                            dump=dump_query,
                            cvat_project=cvat_project_from_datatable,
                            pillar_num=2,
                            status=markup_status_from_datatable_pillar2
                        )
                        db.add(cvat_project_dump2)
                        db.commit()
                    # if list_changes:
                    # db.commit()
                    # logger.info(f'{dump_query.name} will be changed!')
                    # logger.info(" --- ".join(list_of_old_prop))
                    # logger.info(" --- ".join(list_changes))
