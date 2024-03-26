from ..base_model import Base
from sqlalchemy import Column, Integer, String, TIMESTAMP, ForeignKey
from sqlalchemy.orm import relationship 
from sqlalchemy.sql import func
from ..dump_models import geolocation_model
from ..dump_models import system_model
from ..dump_models import ml_purpose_model
# from apps.feature.data_collection_feature.data.models.simulant_models.simulant_dump_model import SimulantDumpModel


class DumpModel(Base):
    __tablename__ = 'dump'
    id = Column(Integer, primary_key = True)
    name = Column(String)
    description = Column(String)
    comment = Column(String)
    geolocation_id = Column(Integer, ForeignKey('geolocation.id'))
    system_id = Column(Integer, ForeignKey('system.id'))
    ml_purpose_id = Column(Integer, ForeignKey('ml_purpose.id'))
    created = Column(TIMESTAMP(True), server_default=func.now())

    geolocation = relationship('geolocation_model.GeolocationModel')
    system = relationship('system_model.SystemModel')
    ml_purpose = relationship('ml_purpose_model.MlPurposeModel')




