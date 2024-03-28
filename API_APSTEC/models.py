from database import Base
from sqlalchemy import Column, Integer, String, TIMESTAMP, ForeignKey, func
from sqlalchemy.orm import relationship


# cvat_project_dump_models (1)


class CvatProjectDumpModel(Base):
    __tablename__ = 'cvat_project_dump'
    id = Column(Integer, primary_key=True)
    dump_id = Column(Integer, ForeignKey('dump.id'))
    cvat_project_id = Column(Integer, ForeignKey('cvat_project.id'))
    status_id = Column(Integer, ForeignKey('markup_status.id'))
    pillar_num = Column(Integer)

    dump = relationship("DumpModel")
    cvat_project = relationship("CvatProjectModel")
    status = relationship("MarkupStatusModel")


class CvatProjectModel(Base):
    __tablename__ = 'cvat_project'
    id = Column(Integer, primary_key=True)
    name = Column(String)


class MarkupStatusModel(Base):
    __tablename__ = 'markup_status'
    id = Column(Integer, primary_key=True)
    name = Column(String)


# dump_models (2)


class DumpModel(Base):
    __tablename__ = 'dump'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    description = Column(String)
    comment = Column(String)
    geolocation_id = Column(Integer, ForeignKey('geolocation.id'))
    system_id = Column(Integer, ForeignKey('system.id'))
    ml_purpose_id = Column(Integer, ForeignKey('ml_purpose.id'))
    created = Column(TIMESTAMP(True), server_default=func.now())

    geolocation = relationship('GeolocationModel')
    system = relationship('SystemModel')
    ml_purpose = relationship('MlPurposeModel')


class GeolocationModel(Base):
    __tablename__ = 'geolocation'
    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True)


class MlPurposeModel(Base):
    __tablename__ = 'ml_purpose'
    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True)


class SystemModel(Base):
    __tablename__ = 'system'
    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True)


# simulant_models (3)


class SimulantDumpModel(Base):
    __tablename__ = 'simulant_dump'
    id = Column(Integer, primary_key=True)
    dump_id = Column(Integer, ForeignKey('dump.id'))
    object_id = Column(Integer, ForeignKey('object.id'))
    vector_id = Column(Integer, ForeignKey('vector.id'))
    locationhrz_id = Column(Integer, ForeignKey('locationhrz.id'))
    locationvrt_id = Column(Integer, ForeignKey('locationvrt.id'))
    orientation_id = Column(Integer, ForeignKey('orientation.id'))

    dump = relationship('DumpModel')
    object = relationship('ObjectModel')
    vector = relationship('VectorModel')
    locationhrz = relationship('LocationHrzModel')
    locationvrt = relationship('LocationVrtModel')
    orientation = relationship('OrientationModel')


class LocationHrzModel(Base):
    __tablename__ = 'locationhrz'
    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True)


class LocationVrtModel(Base):
    __tablename__ = 'locationvrt'
    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True)


class ObjectModel(Base):
    __tablename__ = 'object'
    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True)


class OrientationModel(Base):
    __tablename__ = 'orientation'
    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True)


class VectorModel(Base):
    __tablename__ = 'vector'
    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True)
