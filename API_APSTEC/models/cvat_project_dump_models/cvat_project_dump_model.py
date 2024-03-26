from ..base_model import Base
from sqlalchemy import Column, Integer, ForeignKey, String
from sqlalchemy.orm import relationship 
from ..dump_models import dump_model
# from ..dump_models.dump_model import DumpModel
from . import cvat_project_model, markup_status_model
from .cvat_project_model import CvatProjectModel
from .markup_status_model import MarkupStatusModel



class CvatProjectDumpModel(Base):
    __tablename__ = 'cvat_project_dump'
    id = Column(Integer, primary_key = True)
    dump_id = Column(Integer, ForeignKey('dump.id'))
    cvat_project_id = Column(Integer, ForeignKey('cvat_project.id'))
    status_id = Column(Integer, ForeignKey('markup_status.id'))
    pillar_num = Column(Integer)
    dump = relationship("dump_model.DumpModel")
    cvat_project = relationship("cvat_project_model.CvatProjectModel")
    status = relationship("markup_status_model.MarkupStatusModel")
