from ..base_model import Base
from sqlalchemy import Column, Integer, String


class CvatProjectModel(Base):
    __tablename__ = 'cvat_project'
    id = Column(Integer, primary_key = True)
    name = Column(String)