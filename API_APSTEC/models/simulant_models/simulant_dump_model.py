from ..base_model import Base
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from ..dump_models import dump_model
from ..simulant_models import location_hrz_model, location_vrt_model, objects_model, orientation_model, vector_model

class SimulantDumpModel(Base):
    __tablename__ = 'simulant_dump'
    id = Column(Integer, primary_key = True)
    dump_id = Column(Integer, ForeignKey('dump.id'))
    object_id = Column(Integer, ForeignKey('object.id'))
    vector_id = Column(Integer, ForeignKey('vector.id'))
    locationhrz_id = Column(Integer, ForeignKey('locationhrz.id'))
    locationvrt_id = Column(Integer, ForeignKey('locationvrt.id'))
    orientation_id = Column(Integer, ForeignKey('orientation.id'))

    dump = relationship('dump_model.DumpModel')
    object = relationship('objects_model.ObjectModel')   
    vector = relationship('vector_model.VectorModel')
    locationhrz = relationship('location_hrz_model.LocationHrzModel')
    locationvrt = relationship('location_vrt_model.LocationVrtModel')
    orientation = relationship('orientation_model.OrientationModel')
